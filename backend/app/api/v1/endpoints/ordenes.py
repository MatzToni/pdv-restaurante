from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from decimal import Decimal
from app.db.session import get_db
from app.models.orden import Orden, OrdenItem, EstadoOrden, EstadoOrdenItem
from app.models.mesa import Mesa, EstadoMesa
from app.models.menu import Producto
from app.models.usuario import Usuario, RolUsuario
from app.models.inventario import MovimientoInventario, TipoMovimientoInventario, ArticuloInventario
from app.schemas.orden import (
    OrdenOut,
    OrdenCreate,
    CancelarItemRequest,
    CancelarOrdenRequest,
    CambiarEstadoItemRequest,
    OrdenItemOut
)

router = APIRouter()

@router.get("/activas", response_model=List[OrdenOut], summary="Listar órdenes activas para pantalla de Cocina (KDS) y Salón")
def listar_ordenes_activas(db: Session = Depends(get_db)):
    return db.query(Orden).filter(
        Orden.estado.in_([EstadoOrden.EN_COLA, EstadoOrden.PREPARANDO, EstadoOrden.LISTO, EstadoOrden.ENTREGADO])
    ).order_by(Orden.fecha_apertura.asc()).all()

@router.post("/", response_model=OrdenOut, status_code=status.HTTP_201_CREATED, summary="Crear y enviar comanda a Cocina/Barra")
def crear_orden(orden_in: OrdenCreate, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == orden_in.mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")

    # 1. Crear Orden
    nueva_orden = Orden(
        mesa_id=orden_in.mesa_id,
        mesero_id=orden_in.mesero_id,
        estado=EstadoOrden.EN_COLA,
        notas=orden_in.notas,
        subtotal=Decimal("0.0"),
        total=Decimal("0.0")
    )
    db.add(nueva_orden)
    db.commit()
    db.refresh(nueva_orden)

    subtotal_acumulado = Decimal("0.0")

    # 2. Agregar Items y calcular totales
    for it in orden_in.items:
        prod = db.query(Producto).filter(Producto.id == it.producto_id).first()
        if not prod:
            continue
        
        precio_u = Decimal(str(prod.precio))
        subtotal_item = precio_u * it.cantidad
        subtotal_acumulado += subtotal_item

        item_orden = OrdenItem(
            orden_id=nueva_orden.id,
            producto_id=prod.id,
            cantidad=it.cantidad,
            precio_unitario=precio_u,
            notas=it.notas,
            estado=EstadoOrdenItem.PENDIENTE
        )
        db.add(item_orden)

        # Descontar automáticamente insumos del inventario según la receta
        for item_receta in prod.receta_items:
            articulo = item_receta.articulo
            cantidad_a_descontar = item_receta.cantidad_requerida * it.cantidad
            nuevo_stock = max(Decimal("0.0"), articulo.stock_actual - cantidad_a_descontar)
            articulo.stock_actual = nuevo_stock
            
            mov = MovimientoInventario(
                articulo_id=articulo.id,
                tipo=TipoMovimientoInventario.SALIDA_VENTA,
                cantidad=cantidad_a_descontar,
                stock_resultante=nuevo_stock,
                motivo=f"Venta comanda #{nueva_orden.id} ({prod.nombre})"
            )
            db.add(mov)

    nueva_orden.subtotal = subtotal_acumulado
    nueva_orden.total = subtotal_acumulado

    # Marcar mesa como ocupada
    mesa.estado = EstadoMesa.OCUPADA

    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden

@router.patch("/items/{item_id}/estado", response_model=OrdenItemOut, summary="Cambiar estado de un platillo en cocina")
def cambiar_estado_item(item_id: int, request: CambiarEstadoItemRequest, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")

    item.estado = request.estado
    db.commit()
    db.refresh(item)
    return item

@router.post("/items/{item_id}/cancelar", response_model=OrdenItemOut, summary="Cancelar un platillo con PIN de autorización y registro de merma")
def cancelar_item(item_id: int, request: CancelarItemRequest, db: Session = Depends(get_db)):
    # 1. Validar autorización
    usuario = db.query(Usuario).filter(
        Usuario.pin_seguridad == request.pin_autorizacion,
        Usuario.activo == True,
        Usuario.rol.in_([RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE])
    ).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="PIN no autorizado para cancelar platillos.")

    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")

    item.estado = EstadoOrdenItem.CANCELADO
    item.usuario_cancelo_id = usuario.id
    item.motivo_cancelacion = request.motivo
    item.genera_merma = request.genera_merma

    # Si NO genera merma (la comida no se preparó), regresar los insumos al inventario
    if not request.genera_merma:
        prod = item.producto
        for r in prod.receta_items:
            articulo = r.articulo
            devolucion = r.cantidad_requerida * item.cantidad
            articulo.stock_actual += devolucion
            mov = MovimientoInventario(
                articulo_id=articulo.id,
                usuario_id=usuario.id,
                tipo=TipoMovimientoInventario.AJUSTE,
                cantidad=devolucion,
                stock_resultante=articulo.stock_actual,
                motivo=f"Retorno a stock por cancelación sin merma (Item #{item.id} - {request.motivo})"
            )
            db.add(mov)

    # Recalcular total de la orden
    orden = item.orden
    monto_cancelado = item.precio_unitario * item.cantidad
    orden.subtotal = max(Decimal("0.0"), orden.subtotal - monto_cancelado)
    orden.total = max(Decimal("0.0"), orden.total - monto_cancelado)

    db.commit()
    db.refresh(item)
    return item

@router.post("/{orden_id}/cancelar", response_model=OrdenOut, summary="Cancelar una orden completa")
def cancelar_orden(orden_id: int, request: CancelarOrdenRequest, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.pin_seguridad == request.pin_autorizacion,
        Usuario.activo == True,
        Usuario.rol.in_([RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE])
    ).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="PIN no autorizado para cancelar la orden.")

    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")

    orden.estado = EstadoOrden.CANCELADA
    orden.notas = f"{orden.notas or ''} [CANCELADA por {usuario.nombre}: {request.motivo}]"
    orden.fecha_cierre = datetime.now(timezone.utc)

    # Liberar mesa si no hay otras órdenes activas
    mesa = orden.mesa
    mesa.estado = EstadoMesa.LIBRE

    db.commit()
    db.refresh(orden)
    return orden

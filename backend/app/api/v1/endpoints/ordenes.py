from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
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
    AgregarItemsOrdenRequest,
    CancelarItemRequest,
    DescartarUnidadItemRequest,
    CancelarOrdenRequest,
    CambiarEstadoItemRequest,
    ReportarObservacionItemRequest,
    ResolverObservacionItemRequest,
    OrdenItemOut
)

router = APIRouter()

@router.get("/activas", response_model=List[OrdenOut], summary="Listar órdenes activas para pantalla de Cocina (KDS) y Salón")
def listar_ordenes_activas(db: Session = Depends(get_db)):
    return db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).filter(
        Orden.estado.in_([EstadoOrden.EN_COLA, EstadoOrden.PREPARANDO, EstadoOrden.LISTO, EstadoOrden.ENTREGADO])
    ).order_by(Orden.fecha_apertura.asc()).all()

@router.get("/mesa/{mesa_id}/activa", response_model=Optional[OrdenOut], summary="Obtener comanda activa de una mesa")
def obtener_orden_activa_mesa(mesa_id: int, usuario_id: Optional[int] = None, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if mesa and mesa.mesero_id and usuario_id:
        user = db.query(Usuario).filter(Usuario.id == usuario_id).first()
        if user and user.rol in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL] and mesa.mesero_id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Esta mesa está asignada a {mesa.mesero_nombre or 'otro mesero'}. No tienes permisos para ver sus comandas."
            )

    orden = db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).filter(
        Orden.mesa_id == mesa_id,
        Orden.estado.in_([EstadoOrden.EN_COLA, EstadoOrden.PREPARANDO, EstadoOrden.LISTO, EstadoOrden.ENTREGADO])
    ).first()
    return orden

@router.post("/", response_model=OrdenOut, status_code=status.HTTP_201_CREATED, summary="Crear y enviar comanda a Cocina/Barra con extras")
def crear_orden(orden_in: OrdenCreate, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == orden_in.mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")

    # Validar que otro mesero no tome orden en mesa ajena
    if mesa.mesero_id and mesa.mesero_id != orden_in.mesero_id:
        user = db.query(Usuario).filter(Usuario.id == orden_in.mesero_id).first()
        if user and user.rol in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Esta mesa está asignada a {mesa.mesero_nombre or 'otro colaborador'}. Solo el mesero responsable o jefatura pueden crear comandas en ella."
            )

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

    # 2. Agregar Items con extras y calcular totales
    for it in orden_in.items:
        prod = db.query(Producto).filter(Producto.id == it.producto_id).first()
        if not prod:
            continue
        
        # Calcular extras
        extras_list = [{"nombre": ex.nombre, "precio": float(ex.precio)} for ex in (it.extras or [])]
        costo_extras = sum(Decimal(str(ex["precio"])) for ex in extras_list)
        precio_u = Decimal(str(prod.precio)) + costo_extras
        subtotal_item = precio_u * it.cantidad
        subtotal_acumulado += subtotal_item

        item_orden = OrdenItem(
            orden_id=nueva_orden.id,
            producto_id=prod.id,
            cantidad=it.cantidad,
            precio_unitario=precio_u,
            notas=it.notas,
            extras=extras_list,
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

    # Marcar mesa como ocupada y asignar mesero que tomó la comanda
    mesa.estado = EstadoMesa.OCUPADA
    mesa.mesero_id = orden_in.mesero_id

    db.commit()
    db.refresh(nueva_orden)
    return nueva_orden

@router.post("/{orden_id}/items", response_model=OrdenOut, summary="Agregar más productos/extras a una comanda existente")
def agregar_items_a_orden(orden_id: int, request: AgregarItemsOrdenRequest, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")
    if orden.estado in [EstadoOrden.PAGADO, EstadoOrden.CANCELADA]:
        raise HTTPException(status_code=400, detail="No se pueden agregar productos a una orden cerrada o pagada.")

    # Validar que si quien agrega ronda es un mesero, sea el mesero asignado
    if request.usuario_id:
        user = db.query(Usuario).filter(Usuario.id == request.usuario_id).first()
        mesa_responsable_id = (orden.mesa.mesero_id if orden.mesa else None) or orden.mesero_id
        if mesa_responsable_id and user and user.rol in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL] and mesa_responsable_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Esta mesa está asignada a otro mesero. Solo el mesero responsable o jefatura pueden agregar rondas a esta orden."
            )

    subtotal_adicional = Decimal("0.0")

    for it in request.items:
        prod = db.query(Producto).filter(Producto.id == it.producto_id).first()
        if not prod:
            continue

        extras_list = [{"nombre": ex.nombre, "precio": float(ex.precio)} for ex in (it.extras or [])]
        costo_extras = sum(Decimal(str(ex["precio"])) for ex in extras_list)
        precio_u = Decimal(str(prod.precio)) + costo_extras
        subtotal_item = precio_u * it.cantidad
        subtotal_adicional += subtotal_item

        item_orden = OrdenItem(
            orden_id=orden.id,
            producto_id=prod.id,
            cantidad=it.cantidad,
            precio_unitario=precio_u,
            notas=it.notas,
            extras=extras_list,
            estado=EstadoOrdenItem.PENDIENTE
        )
        db.add(item_orden)

        # Descontar insumos
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
                motivo=f"Ronda extra comanda #{orden.id} ({prod.nombre})"
            )
            db.add(mov)

    orden.subtotal += subtotal_adicional
    orden.total += subtotal_adicional

    # Si la orden ya estaba lista o entregada, la reactivamos para cocina
    if orden.estado in [EstadoOrden.LISTO, EstadoOrden.ENTREGADO]:
        orden.estado = EstadoOrden.PREPARANDO

    db.commit()
    db.refresh(orden)
    return orden

@router.patch("/items/{item_id}/estado", response_model=OrdenItemOut, summary="Cambiar estado de un platillo en cocina")
def cambiar_estado_item(item_id: int, request: CambiarEstadoItemRequest, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")

    item.estado = request.estado

    # Auto actualizar estado de la orden general
    orden = item.orden
    if orden:
        activos = [it for it in orden.items if it.estado != EstadoOrdenItem.CANCELADO]
        if activos:
            if all(it.estado == EstadoOrdenItem.ENTREGADO for it in activos):
                orden.estado = EstadoOrden.ENTREGADO
            elif all(it.estado in [EstadoOrdenItem.LISTO, EstadoOrdenItem.ENTREGADO] for it in activos):
                orden.estado = EstadoOrden.LISTO
            elif any(it.estado in [EstadoOrdenItem.PREPARANDO, EstadoOrdenItem.EN_OBSERVACION] for it in activos):
                orden.estado = EstadoOrden.PREPARANDO

    db.commit()
    db.refresh(item)
    return item

@router.post("/items/{item_id}/observacion", response_model=OrdenItemOut, summary="Cocina reporta observación o falta de ingrediente")
def reportar_observacion_item(item_id: int, request: ReportarObservacionItemRequest, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")

    item.estado = EstadoOrdenItem.EN_OBSERVACION
    item.observacion_cocina = request.observacion

    orden = item.orden
    if orden and orden.estado == EstadoOrden.EN_COLA:
        orden.estado = EstadoOrden.PREPARANDO

    db.commit()
    db.refresh(item)
    return item

@router.post("/items/{item_id}/resolver-observacion", response_model=OrdenItemOut, summary="Mesero resuelve la aclaración o sustituye/cancela")
def resolver_observacion_item(item_id: int, request: ResolverObservacionItemRequest, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")

    if request.accion == "continuar":
        item.estado = EstadoOrdenItem.PREPARANDO
        if request.respuesta:
            item.notas = f"{item.notas or ''} [Aclaración: {request.respuesta}]".strip()
    elif request.accion == "cancelar":
        item.estado = EstadoOrdenItem.CANCELADO
        item.motivo_cancelacion = f"Cancelado por falta/observación: {item.observacion_cocina}"
        item.genera_merma = False

        # Regresar insumos
        prod = item.producto
        for r in prod.receta_items:
            articulo = r.articulo
            devolucion = r.cantidad_requerida * item.cantidad
            articulo.stock_actual += devolucion
            mov = MovimientoInventario(
                articulo_id=articulo.id,
                tipo=TipoMovimientoInventario.AJUSTE,
                cantidad=devolucion,
                stock_resultante=articulo.stock_actual,
                motivo=f"Retorno stock por cancelación en observación #{item.id}"
            )
            db.add(mov)

        # Restar monto
        orden = item.orden
        monto_cancelado = item.precio_unitario * item.cantidad
        orden.subtotal = max(Decimal("0.0"), orden.subtotal - monto_cancelado)
        orden.total = max(Decimal("0.0"), orden.total - monto_cancelado)

    db.commit()
    db.refresh(item)
    return item

@router.post("/items/{item_id}/descartar-unidad", response_model=OrdenOut, summary="Descartar una sola porción o platillo cuando son múltiples iguales")
def descartar_unidad_item(item_id: int, request: DescartarUnidadItemRequest, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")
    if item.cantidad <= 1:
        raise HTTPException(status_code=400, detail="Este item solo tiene 1 porción. Usa cancelar item.")

    orden = item.orden

    # 1. Reducir 1 unidad del item actual
    item.cantidad -= 1

    # 2. Descontar el precio de 1 unidad del total de la orden
    orden.subtotal = max(Decimal("0.0"), orden.subtotal - item.precio_unitario)
    orden.total = max(Decimal("0.0"), orden.total - item.precio_unitario)

    # 3. Registrar insumos devueltos si no genera merma
    if not request.genera_merma and item.producto:
        for r in item.producto.receta_items:
            articulo = r.articulo
            devolucion = r.cantidad_requerida * 1
            articulo.stock_actual += devolucion
            mov = MovimientoInventario(
                articulo_id=articulo.id,
                tipo=TipoMovimientoInventario.AJUSTE,
                cantidad=devolucion,
                stock_resultante=articulo.stock_actual,
                motivo=f"Retorno stock por descarte de 1 porción en cocina (Item #{item.id} - {item.producto.nombre})"
            )
            db.add(mov)

    # 4. Crear registro del item cancelado para trazabilidad y auditoría
    item_cancelado = OrdenItem(
        orden_id=orden.id,
        producto_id=item.producto_id,
        cantidad=1,
        precio_unitario=item.precio_unitario,
        notas=item.notas,
        extras=item.extras,
        estado=EstadoOrdenItem.CANCELADO,
        motivo_cancelacion=request.motivo or "Descartado 1 unidad en cocina",
        genera_merma=request.genera_merma
    )
    db.add(item_cancelado)

    db.commit()
    db.refresh(orden)
    return orden

@router.post("/items/{item_id}/separar", response_model=OrdenOut, summary="Separar platillos múltiples en items individuales de 1 porción")
def separar_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(OrdenItem).filter(OrdenItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado.")
    if item.cantidad <= 1:
        raise HTTPException(status_code=400, detail="El platillo ya es una sola porción.")

    orden = item.orden

    # Reducir 1 unidad del item original
    item.cantidad -= 1

    # Crear nuevo item con 1 porción
    nuevo_item = OrdenItem(
        orden_id=orden.id,
        producto_id=item.producto_id,
        cantidad=1,
        precio_unitario=item.precio_unitario,
        notas=item.notas,
        extras=item.extras,
        estado=item.estado
    )
    db.add(nuevo_item)

    db.commit()
    db.refresh(orden)
    return orden

@router.post("/{orden_id}/pedir-cuenta", response_model=OrdenOut, summary="Marcar mesa para cobro de cuenta")
def pedir_cuenta_orden(orden_id: int, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")

    mesa = orden.mesa
    if mesa:
        mesa.estado = EstadoMesa.CUENTA

    db.commit()
    db.refresh(orden)
    return orden

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
    if mesa:
        mesa.estado = EstadoMesa.LIBRE

    db.commit()
    db.refresh(orden)
    return orden

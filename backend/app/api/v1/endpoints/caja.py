from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timezone, date
from decimal import Decimal
from app.db.session import get_db
from app.models.caja import Pago, MetodoPago, CajaTurno, EstadoCaja
from app.models.orden import Orden, OrdenItem, EstadoOrden, EstadoOrdenItem
from app.models.mesa import Mesa, EstadoMesa
from app.models.usuario import Usuario
from app.schemas.caja import PagoCreate, PagoOut, ResumenCorteX, CajaTurnoCreate, CajaTurnoCierre, CajaTurnoOut, AplicarDescuentoRequest
from app.schemas.orden import OrdenOut

router = APIRouter()

@router.get("/cuentas-pendientes", response_model=List[OrdenOut], summary="Listar órdenes en espera de pago (mesas por cobrar y pedidos para llevar/envío)")
def listar_cuentas_pendientes(db: Session = Depends(get_db)):
    from sqlalchemy import or_, case
    # Priorizar mesas con estado cuenta (que pidieron la cuenta), luego para llevar/envío, luego comedor activo
    prioridad_cuenta = case(
        (Mesa.estado == EstadoMesa.CUENTA, 1),
        (Orden.tipo_pedido.in_(["para_llevar", "domicilio"]), 2),
        else_=3
    )
    return db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).outerjoin(Mesa).filter(
        Orden.estado.in_([EstadoOrden.ENTREGADO, EstadoOrden.LISTO, EstadoOrden.PREPARANDO, EstadoOrden.EN_COLA]),
        Orden.items.any(OrdenItem.estado != EstadoOrdenItem.CANCELADO),
        or_(
            Mesa.estado == EstadoMesa.CUENTA,
            Orden.tipo_pedido.in_(["para_llevar", "domicilio"]),
            Mesa.estado == EstadoMesa.OCUPADA
        )
    ).order_by(prioridad_cuenta, Orden.fecha_apertura.desc()).all()

@router.post("/cobrar", response_model=PagoOut, status_code=status.HTTP_201_CREATED, summary="Procesar pago de una orden y liberar mesa")
def cobrar_orden(pago_in: PagoCreate, db: Session = Depends(get_db)):
    orden = db.query(Orden).filter(Orden.id == pago_in.orden_id).first()
    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")
    if orden.estado == EstadoOrden.PAGADO:
        raise HTTPException(status_code=400, detail="Esta orden ya fue liquidada.")

    monto_total_requerido = orden.total + pago_in.propina

    # En efectivo se calcula cambio
    cambio = Decimal("0.0")
    if pago_in.metodo == MetodoPago.EFECTIVO:
        if pago_in.monto_recibido < monto_total_requerido:
            raise HTTPException(
                status_code=400, 
                detail=f"Monto recibido (${pago_in.monto_recibido}) insuficiente para cubrir el total (${monto_total_requerido})."
            )
        cambio = pago_in.monto_recibido - monto_total_requerido
    else:
        # En tarjeta o transferencia el monto recibido es el exacto
        pago_in.monto_recibido = monto_total_requerido

    # Asociar automáticamente al turno de caja abierto si no se especificó uno
    caja_turno_id = pago_in.caja_turno_id
    if not caja_turno_id:
        turno_activo = db.query(CajaTurno).filter(CajaTurno.estado == EstadoCaja.ABIERTA).order_by(CajaTurno.fecha_apertura.desc()).first()
        if turno_activo:
            caja_turno_id = turno_activo.id

    nuevo_pago = Pago(
        orden_id=orden.id,
        caja_turno_id=caja_turno_id,
        monto=orden.total,
        metodo=pago_in.metodo,
        propina=pago_in.propina,
        cambio=cambio
    )
    db.add(nuevo_pago)

    # Actualizar orden
    orden.estado = EstadoOrden.PAGADO
    orden.fecha_cierre = datetime.now(timezone.utc)

    # Liberar la mesa y desasignar al mesero (se desasigna hasta que se realice el pago)
    mesa = orden.mesa
    if mesa:
        mesa.estado = EstadoMesa.LIBRE
        mesa.mesero_id = None

    db.commit()
    db.refresh(nuevo_pago)
    return nuevo_pago

@router.post("/aplicar-descuento", response_model=OrdenOut, summary="Aplicar descuento o cupón a una orden pendiente")
def aplicar_descuento_orden(req: AplicarDescuentoRequest, db: Session = Depends(get_db)):
    orden = db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).filter(Orden.id == req.orden_id).first()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")
    if orden.estado in [EstadoOrden.PAGADO, EstadoOrden.CANCELADA]:
        raise HTTPException(status_code=400, detail="No se puede aplicar descuento a una comanda ya pagada o cancelada.")

    # Si se proporcionó un PIN de autorización, validarlo
    if req.pin_autorizacion:
        from app.models.usuario import RolUsuario
        valido = db.query(Usuario).filter(
            Usuario.pin_seguridad == str(req.pin_autorizacion).strip(),
            Usuario.activo == True,
            Usuario.rol.in_([RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE])
        ).first()
        if not valido:
            raise HTTPException(status_code=403, detail="PIN de autorización inválido o sin permisos.")

    cupones_conocidos = {
        "EDEN10": Decimal("10.0"),
        "EDEN15": Decimal("15.0"),
        "BIENVENIDA": Decimal("15.0"),
        "PROMO20": Decimal("20.0"),
        "CAFE50": Decimal("50.0")
    }

    subtotal_prods = orden.subtotal
    monto_descuento = Decimal("0.0")

    if req.tipo_descuento == "cupon":
        cod = (req.cupon or "").strip().upper()
        if cod == "CAFE50":
            monto_descuento = Decimal("50.0")
        elif cod in cupones_conocidos:
            pct = cupones_conocidos[cod]
            monto_descuento = (subtotal_prods * pct) / Decimal("100.0")
        elif req.valor > 0:
            monto_descuento = req.valor
        else:
            raise HTTPException(status_code=400, detail=f"Cupón '{cod}' no válido o no reconocido.")
    elif req.tipo_descuento == "porcentaje":
        pct = max(Decimal("0.0"), min(Decimal("100.0"), req.valor))
        monto_descuento = (subtotal_prods * pct) / Decimal("100.0")
    elif req.tipo_descuento == "fijo":
        monto_descuento = max(Decimal("0.0"), req.valor)

    monto_descuento = min(subtotal_prods, max(Decimal("0.0"), monto_descuento))

    orden.descuento = round(monto_descuento, 2)
    orden.total = max(Decimal("0.0"), orden.subtotal + orden.costo_envio - orden.descuento)

    if req.motivo or req.cupon:
        detalle = f"Descuento: {req.motivo or req.cupon}"
        if not orden.notas:
            orden.notas = f"[{detalle}]"
        elif detalle not in orden.notas:
            orden.notas = f"{orden.notas} [{detalle}]"

    db.commit()
    db.refresh(orden)
    return orden

@router.delete("/quitar-descuento/{orden_id}", response_model=OrdenOut, summary="Quitar descuento de una orden")
def quitar_descuento_orden(orden_id: int, db: Session = Depends(get_db)):
    orden = db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).filter(Orden.id == orden_id).first()

    if not orden:
        raise HTTPException(status_code=404, detail="Orden no encontrada.")
    if orden.estado in [EstadoOrden.PAGADO, EstadoOrden.CANCELADA]:
        raise HTTPException(status_code=400, detail="No se puede modificar una orden ya liquidada.")

    orden.descuento = Decimal("0.0")
    orden.total = max(Decimal("0.0"), orden.subtotal + orden.costo_envio)

    db.commit()
    db.refresh(orden)
    return orden

@router.get("/corte-x", response_model=ResumenCorteX, summary="Obtener arqueo parcial de caja (Corte X)")
def obtener_corte_x(db: Session = Depends(get_db)):
    # Buscar si hay un turno activo para acotar el corte al turno, o al día de hoy
    turno_activo = db.query(CajaTurno).filter(CajaTurno.estado == EstadoCaja.ABIERTA).order_by(CajaTurno.fecha_apertura.desc()).first()

    if turno_activo:
        pagos = db.query(Pago).filter(Pago.fecha >= turno_activo.fecha_apertura).all()
        monto_apertura = turno_activo.monto_apertura
    else:
        hoy = date.today()
        pagos = db.query(Pago).filter(
            Pago.fecha >= datetime(hoy.year, hoy.month, hoy.day, 0, 0, 0, tzinfo=timezone.utc)
        ).all()
        monto_apertura = Decimal("0.0")

    total_efectivo = Decimal("0.0")
    total_tarjeta = Decimal("0.0")
    total_transferencia = Decimal("0.0")
    total_propinas = Decimal("0.0")

    for p in pagos:
        total_propinas += p.propina
        if p.metodo == MetodoPago.EFECTIVO:
            total_efectivo += p.monto
        elif p.metodo == MetodoPago.TARJETA:
            total_tarjeta += p.monto
        elif p.metodo == MetodoPago.TRANSFERENCIA:
            total_transferencia += p.monto

    gran_total = total_efectivo + total_tarjeta + total_transferencia
    total_efectivo_en_caja = monto_apertura + total_efectivo

    return ResumenCorteX(
        fecha_corte=datetime.now(timezone.utc),
        total_efectivo=total_efectivo,
        total_tarjeta=total_tarjeta,
        total_transferencia=total_transferencia,
        total_propinas=total_propinas,
        gran_total=gran_total,
        ordenes_cobradas=len(pagos),
        monto_apertura=monto_apertura,
        total_efectivo_en_caja=total_efectivo_en_caja
    )

@router.get("/turno-activo", summary="Consultar turno de caja abierto actualmente")
def obtener_turno_activo(db: Session = Depends(get_db)):
    turno = db.query(CajaTurno).options(joinedload(CajaTurno.usuario)).filter(
        CajaTurno.estado == EstadoCaja.ABIERTA
    ).order_by(CajaTurno.fecha_apertura.desc()).first()

    if not turno:
        return None

    pagos = db.query(Pago).filter(Pago.fecha >= turno.fecha_apertura).all()
    total_efectivo = sum((p.monto for p in pagos if p.metodo == MetodoPago.EFECTIVO), Decimal("0.0"))
    total_tarjeta = sum((p.monto for p in pagos if p.metodo == MetodoPago.TARJETA), Decimal("0.0"))
    total_transferencia = sum((p.monto for p in pagos if p.metodo == MetodoPago.TRANSFERENCIA), Decimal("0.0"))
    total_propinas = sum((p.propina for p in pagos), Decimal("0.0"))
    gran_total = total_efectivo + total_tarjeta + total_transferencia

    return {
        "id": turno.id,
        "usuario_id": turno.usuario_id,
        "usuario_nombre": turno.usuario_nombre,
        "monto_apertura": turno.monto_apertura,
        "fecha_apertura": turno.fecha_apertura,
        "estado": turno.estado,
        "notas": turno.notas,
        "total_efectivo": total_efectivo,
        "total_tarjeta": total_tarjeta,
        "total_transferencia": total_transferencia,
        "total_propinas": total_propinas,
        "gran_total": gran_total,
        "total_efectivo_en_caja": turno.monto_apertura + total_efectivo,
        "ordenes_cobradas": len(pagos)
    }

@router.post("/abrir-turno", summary="Abrir un nuevo turno de caja con fondo inicial")
def abrir_turno(datos: CajaTurnoCreate, db: Session = Depends(get_db)):
    turno_existente = db.query(CajaTurno).filter(CajaTurno.estado == EstadoCaja.ABIERTA).first()
    if turno_existente:
        raise HTTPException(status_code=400, detail="Ya existe un turno de caja abierto actualmente.")

    usuario_id = datos.usuario_id
    if not usuario_id:
        primer_usuario = db.query(Usuario).filter(Usuario.activo == True).first()
        usuario_id = primer_usuario.id if primer_usuario else 1

    nuevo_turno = CajaTurno(
        usuario_id=usuario_id,
        monto_apertura=datos.monto_apertura,
        notas=datos.notas,
        estado=EstadoCaja.ABIERTA
    )
    db.add(nuevo_turno)
    db.commit()
    db.refresh(nuevo_turno)
    return {
        "id": nuevo_turno.id,
        "usuario_id": nuevo_turno.usuario_id,
        "monto_apertura": nuevo_turno.monto_apertura,
        "fecha_apertura": nuevo_turno.fecha_apertura,
        "estado": nuevo_turno.estado,
        "notas": nuevo_turno.notas
    }

@router.post("/cerrar-turno", summary="Cerrar turno de caja definitivo (Corte Z)")
def cerrar_turno(datos: CajaTurnoCierre, db: Session = Depends(get_db)):
    turno = db.query(CajaTurno).options(joinedload(CajaTurno.usuario)).filter(
        CajaTurno.estado == EstadoCaja.ABIERTA
    ).order_by(CajaTurno.fecha_apertura.desc()).first()

    if not turno:
        raise HTTPException(status_code=400, detail="No hay ningún turno de caja abierto para cerrar.")

    pagos = db.query(Pago).filter(Pago.fecha >= turno.fecha_apertura).all()
    total_efectivo = sum((p.monto for p in pagos if p.metodo == MetodoPago.EFECTIVO), Decimal("0.0"))
    total_tarjeta = sum((p.monto for p in pagos if p.metodo == MetodoPago.TARJETA), Decimal("0.0"))
    total_transferencia = sum((p.monto for p in pagos if p.metodo == MetodoPago.TRANSFERENCIA), Decimal("0.0"))
    total_propinas = sum((p.propina for p in pagos), Decimal("0.0"))
    gran_total = total_efectivo + total_tarjeta + total_transferencia

    efectivo_esperado_sistema = turno.monto_apertura + total_efectivo
    diferencia = datos.monto_cierre_declarado - efectivo_esperado_sistema

    turno.fecha_cierre = datetime.now(timezone.utc)
    turno.monto_cierre_declarado = datos.monto_cierre_declarado
    turno.monto_cierre_sistema = efectivo_esperado_sistema
    turno.estado = EstadoCaja.CERRADA
    if datos.notas:
        turno.notas = f"{turno.notas or ''} | Cierre: {datos.notas}".strip()

    db.commit()
    db.refresh(turno)

    return {
        "id": turno.id,
        "usuario_id": turno.usuario_id,
        "usuario_nombre": turno.usuario_nombre,
        "monto_apertura": turno.monto_apertura,
        "fecha_apertura": turno.fecha_apertura,
        "fecha_cierre": turno.fecha_cierre,
        "monto_cierre_declarado": turno.monto_cierre_declarado,
        "monto_cierre_sistema": turno.monto_cierre_sistema,
        "diferencia": diferencia,
        "estado": turno.estado,
        "total_efectivo": total_efectivo,
        "total_tarjeta": total_tarjeta,
        "total_transferencia": total_transferencia,
        "total_propinas": total_propinas,
        "gran_total": gran_total,
        "ordenes_cobradas": len(pagos),
        "notas": turno.notas
    }

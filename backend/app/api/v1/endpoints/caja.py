from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from datetime import datetime, timezone, date
from decimal import Decimal
from app.db.session import get_db
from app.models.caja import Pago, MetodoPago, CajaTurno, EstadoCaja
from app.models.orden import Orden, OrdenItem, EstadoOrden
from app.models.mesa import Mesa, EstadoMesa
from app.schemas.caja import PagoCreate, PagoOut, ResumenCorteX
from app.schemas.orden import OrdenOut

router = APIRouter()

@router.get("/cuentas-pendientes", response_model=List[OrdenOut], summary="Listar órdenes en espera de pago (mesas por cobrar)")
def listar_cuentas_pendientes(db: Session = Depends(get_db)):
    # Mesas con estado cuenta o órdenes entregadas pendientes de pago
    return db.query(Orden).options(
        joinedload(Orden.mesa),
        joinedload(Orden.mesero),
        joinedload(Orden.items).joinedload(OrdenItem.producto)
    ).join(Mesa).filter(
        Orden.estado.in_([EstadoOrden.ENTREGADO, EstadoOrden.LISTO, EstadoOrden.PREPARANDO, EstadoOrden.EN_COLA]),
        Mesa.estado.in_([EstadoMesa.CUENTA, EstadoMesa.OCUPADA])
    ).order_by(Mesa.id.asc()).all()

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

    nuevo_pago = Pago(
        orden_id=orden.id,
        caja_turno_id=pago_in.caja_turno_id,
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

@router.get("/corte-x", response_model=ResumenCorteX, summary="Obtener arqueo parcial de caja (Corte X)")
def obtener_corte_x(db: Session = Depends(get_db)):
    hoy = date.today()
    pagos_hoy = db.query(Pago).filter(
        Pago.fecha >= datetime(hoy.year, hoy.month, hoy.day, 0, 0, 0, tzinfo=timezone.utc)
    ).all()

    total_efectivo = Decimal("0.0")
    total_tarjeta = Decimal("0.0")
    total_transferencia = Decimal("0.0")
    total_propinas = Decimal("0.0")

    for p in pagos_hoy:
        total_propinas += p.propina
        if p.metodo == MetodoPago.EFECTIVO:
            total_efectivo += p.monto
        elif p.metodo == MetodoPago.TARJETA:
            total_tarjeta += p.monto
        elif p.metodo == MetodoPago.TRANSFERENCIA:
            total_transferencia += p.monto

    gran_total = total_efectivo + total_tarjeta + total_transferencia

    return ResumenCorteX(
        fecha_corte=datetime.now(timezone.utc),
        total_efectivo=total_efectivo,
        total_tarjeta=total_tarjeta,
        total_transferencia=total_transferencia,
        total_propinas=total_propinas,
        gran_total=gran_total,
        ordenes_cobradas=len(pagos_hoy)
    )

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.models.caja import MetodoPago, EstadoCaja
from app.schemas.orden import OrdenOut

class PagoCreate(BaseModel):
    orden_id: int
    metodo: MetodoPago = MetodoPago.EFECTIVO
    monto_recibido: Decimal
    propina: Decimal = Decimal("0.0")
    caja_turno_id: Optional[int] = None

class PagoOut(BaseModel):
    id: int
    orden_id: int
    caja_turno_id: Optional[int] = None
    monto: Decimal
    metodo: MetodoPago
    propina: Decimal
    cambio: Decimal
    fecha: datetime

    class Config:
        from_attributes = True

class ResumenCorteX(BaseModel):
    fecha_corte: datetime
    total_efectivo: Decimal
    total_tarjeta: Decimal
    total_transferencia: Decimal
    total_propinas: Decimal
    gran_total: Decimal
    ordenes_cobradas: int

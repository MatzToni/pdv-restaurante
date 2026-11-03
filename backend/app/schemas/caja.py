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
    monto_apertura: Optional[Decimal] = Decimal("0.0")
    total_efectivo_en_caja: Optional[Decimal] = Decimal("0.0")

class CajaTurnoCreate(BaseModel):
    monto_apertura: Decimal = Decimal("0.0")
    usuario_id: Optional[int] = None
    notas: Optional[str] = None

class CajaTurnoCierre(BaseModel):
    monto_cierre_declarado: Decimal
    notas: Optional[str] = None

class CajaTurnoOut(BaseModel):
    id: int
    usuario_id: int
    usuario_nombre: Optional[str] = None
    monto_apertura: Decimal
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime] = None
    monto_cierre_declarado: Optional[Decimal] = None
    monto_cierre_sistema: Optional[Decimal] = None
    estado: EstadoCaja
    notas: Optional[str] = None
    total_efectivo: Optional[Decimal] = Decimal("0.0")
    total_tarjeta: Optional[Decimal] = Decimal("0.0")
    total_transferencia: Optional[Decimal] = Decimal("0.0")
    total_propinas: Optional[Decimal] = Decimal("0.0")
    gran_total: Optional[Decimal] = Decimal("0.0")
    diferencia: Optional[Decimal] = Decimal("0.0")
    ordenes_cobradas: Optional[int] = 0

    class Config:
        from_attributes = True

class AplicarDescuentoRequest(BaseModel):
    orden_id: int
    tipo_descuento: str = "porcentaje" # "porcentaje", "fijo", "cupon"
    valor: Decimal = Decimal("0.0")
    cupon: Optional[str] = None
    motivo: Optional[str] = None
    pin_autorizacion: Optional[str] = None

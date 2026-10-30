from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal
from datetime import datetime
from app.models.orden import EstadoOrden, EstadoOrdenItem

class OrdenItemCreate(BaseModel):
    producto_id: int
    cantidad: int = 1
    notas: Optional[str] = None

class OrdenItemOut(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal
    notas: Optional[str] = None
    estado: EstadoOrdenItem
    motivo_cancelacion: Optional[str] = None
    genera_merma: bool = False

    class Config:
        from_attributes = True

class CancelarItemRequest(BaseModel):
    pin_autorizacion: str
    motivo: str
    genera_merma: bool = False

class OrdenCreate(BaseModel):
    mesa_id: int
    mesero_id: int
    notas: Optional[str] = None
    items: List[OrdenItemCreate]

class CancelarOrdenRequest(BaseModel):
    pin_autorizacion: str
    motivo: str

class CambiarEstadoItemRequest(BaseModel):
    estado: EstadoOrdenItem

class OrdenOut(BaseModel):
    id: int
    mesa_id: int
    mesero_id: int
    estado: EstadoOrden
    notas: Optional[str] = None
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime] = None
    items: List[OrdenItemOut] = []

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, List, Any
from decimal import Decimal
from datetime import datetime
from app.models.orden import EstadoOrden, EstadoOrdenItem

class ExtraItem(BaseModel):
    nombre: str
    precio: Decimal = Decimal("0.0")

class OrdenItemCreate(BaseModel):
    producto_id: int
    cantidad: int = 1
    notas: Optional[str] = None
    extras: Optional[List[ExtraItem]] = []

class OrdenItemOut(BaseModel):
    id: int
    producto_id: int
    producto_nombre: Optional[str] = None
    cantidad: int
    precio_unitario: Decimal
    notas: Optional[str] = None
    extras: Optional[List[Any]] = []
    observacion_cocina: Optional[str] = None
    estado: EstadoOrdenItem
    motivo_cancelacion: Optional[str] = None
    genera_merma: bool = False

    class Config:
        from_attributes = True

class CancelarItemRequest(BaseModel):
    pin_autorizacion: str
    motivo: str
    genera_merma: bool = False

class ReportarObservacionItemRequest(BaseModel):
    observacion: str

class ResolverObservacionItemRequest(BaseModel):
    accion: str # "continuar" o "cancelar"
    respuesta: Optional[str] = None

class OrdenCreate(BaseModel):
    mesa_id: int
    mesero_id: int
    notas: Optional[str] = None
    items: List[OrdenItemCreate]

class AgregarItemsOrdenRequest(BaseModel):
    items: List[OrdenItemCreate]

class CancelarOrdenRequest(BaseModel):
    pin_autorizacion: str
    motivo: str

class CambiarEstadoItemRequest(BaseModel):
    estado: EstadoOrdenItem

class OrdenOut(BaseModel):
    id: int
    mesa_id: int
    mesa_numero: Optional[str] = None
    mesero_id: int
    mesero_nombre: Optional[str] = None
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

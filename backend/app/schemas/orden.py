from pydantic import BaseModel, Field
from typing import Optional, List, Any
from decimal import Decimal
from datetime import datetime
from app.models.orden import EstadoOrden, EstadoOrdenItem

class ExtraItem(BaseModel):
    nombre: str = Field(..., max_length=80)
    precio: Decimal = Decimal("0.0")

class OrdenItemCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(1, ge=1, le=100)
    notas: Optional[str] = Field(None, max_length=150)
    extras: Optional[List[ExtraItem]] = []
    para_llevar: bool = False
    cargo_desechable: Decimal = Decimal("0.0")

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
    para_llevar: bool = False
    cargo_desechable: Decimal = Decimal("0.0")

    class Config:
        from_attributes = True

class CancelarItemRequest(BaseModel):
    pin_autorizacion: str = Field(..., max_length=10)
    motivo: str = Field(..., max_length=150)
    genera_merma: bool = False

class DescartarUnidadItemRequest(BaseModel):
    motivo: Optional[str] = Field("Descartada 1 porción en cocina", max_length=150)
    genera_merma: bool = False

class ReportarObservacionItemRequest(BaseModel):
    observacion: str = Field(..., max_length=200)

class ResolverObservacionItemRequest(BaseModel):
    accion: str # "continuar" o "cancelar"
    respuesta: Optional[str] = Field(None, max_length=200)

class OrdenCreate(BaseModel):
    mesa_id: Optional[int] = None
    mesero_id: int
    tipo_pedido: str = "comedor" # "comedor", "para_llevar", "domicilio"
    costo_envio: Decimal = Decimal("0.0")
    datos_entrega: Optional[dict] = None
    notas: Optional[str] = Field(None, max_length=200)
    items: List[OrdenItemCreate]

class AgregarItemsOrdenRequest(BaseModel):
    items: List[OrdenItemCreate]
    usuario_id: Optional[int] = None

class CancelarOrdenRequest(BaseModel):
    pin_autorizacion: Optional[str] = Field(None, max_length=10)
    motivo: str = Field(..., max_length=150)
    genera_merma: bool = False

class CambiarEstadoItemRequest(BaseModel):
    estado: EstadoOrdenItem

class OrdenOut(BaseModel):
    id: int
    mesa_id: Optional[int] = None
    mesa_numero: Optional[str] = None
    mesa_estado: Optional[str] = None
    mesero_id: int
    mesero_nombre: Optional[str] = None
    estado: EstadoOrden
    tipo_pedido: str = "comedor"
    costo_envio: Decimal = Decimal("0.0")
    datos_entrega: Optional[dict] = None
    notas: Optional[str] = None
    subtotal: Decimal
    descuento: Decimal
    total: Decimal
    fecha_apertura: datetime
    fecha_cierre: Optional[datetime] = None
    items: List[OrdenItemOut] = []

    class Config:
        from_attributes = True

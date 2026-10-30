from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime
from app.models.inventario import TipoArticulo, TipoMovimientoInventario

class ArticuloInventarioBase(BaseModel):
    codigo: Optional[str] = None
    nombre: str
    tipo: TipoArticulo = TipoArticulo.INGREDIENTE
    unidad_medida: str
    stock_actual: Decimal = Decimal("0.0")
    stock_minimo: Decimal = Decimal("0.0")
    costo_unitario: Decimal = Decimal("0.0")

class ArticuloInventarioCreate(ArticuloInventarioBase):
    pass

class ArticuloInventarioOut(ArticuloInventarioBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class MovimientoInventarioCreate(BaseModel):
    articulo_id: int
    tipo: TipoMovimientoInventario
    cantidad: Decimal
    motivo: Optional[str] = None

class MovimientoInventarioOut(BaseModel):
    id: int
    articulo_id: int
    usuario_id: Optional[int]
    tipo: TipoMovimientoInventario
    cantidad: Decimal
    stock_resultante: Decimal
    motivo: Optional[str]
    fecha: datetime

    class Config:
        from_attributes = True

from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    orden: int = 0

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class RecetaItemCreate(BaseModel):
    articulo_id: int
    cantidad_requerida: Decimal

class RecetaItemOut(BaseModel):
    id: int
    articulo_id: int
    cantidad_requerida: Decimal

    class Config:
        from_attributes = True

class ProductoBase(BaseModel):
    categoria_id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: Decimal
    disponible: bool = True
    requiere_cocina: bool = True
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    receta: Optional[List[RecetaItemCreate]] = []

class ProductoOut(ProductoBase):
    id: int
    receta_items: Optional[List[RecetaItemOut]] = []

    class Config:
        from_attributes = True

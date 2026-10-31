from pydantic import BaseModel
from typing import Optional, List
from decimal import Decimal

class CategoriaBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    orden: int = 0

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    orden: Optional[int] = None
    activo: Optional[bool] = None

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
    tipo_item: Optional[str] = "platillo" # platillo, bebida, producto, servicio
    descripcion: Optional[str] = None
    precio: Decimal
    disponible: bool = True
    requiere_cocina: bool = True
    imagen_url: Optional[str] = None

class ProductoCreate(ProductoBase):
    receta: Optional[List[RecetaItemCreate]] = []

class ProductoUpdate(BaseModel):
    categoria_id: Optional[int] = None
    nombre: Optional[str] = None
    tipo_item: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    disponible: Optional[bool] = None
    requiere_cocina: Optional[bool] = None
    imagen_url: Optional[str] = None

class ProductoOut(ProductoBase):
    id: int
    categoria_nombre: Optional[str] = None
    receta_items: Optional[List[RecetaItemOut]] = []

    class Config:
        from_attributes = True

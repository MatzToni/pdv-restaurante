from pydantic import BaseModel
from typing import Optional, List, Dict, Any
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
    activo: bool = True
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
    activo: Optional[bool] = None
    requiere_cocina: Optional[bool] = None
    imagen_url: Optional[str] = None

class ProductoOut(ProductoBase):
    id: int
    categoria_nombre: Optional[str] = None
    receta_items: Optional[List[RecetaItemOut]] = []

    class Config:
        from_attributes = True

# --- MENÚ DEL DÍA (COMIDA CORRIDA) ---

class MenuDelDiaConfigBase(BaseModel):
    activo: bool = True
    nombre: str = "Menú del Día (Comida Corrida)"
    descripcion: Optional[str] = None
    precio: Decimal = Decimal("95.00")
    hora_inicio: str = "12:00"
    hora_fin: str = "18:00"
    entradas: List[str] = []
    platos_fuertes: List[str] = []
    guarniciones: List[str] = []
    bebidas: List[str] = []
    postres: List[str] = []
    comidas_corridas: List[Dict[str, Any]] = []

class MenuDelDiaConfigOut(MenuDelDiaConfigBase):
    id: int

    class Config:
        from_attributes = True

class MenuDelDiaConfigUpdate(BaseModel):
    activo: Optional[bool] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    entradas: Optional[List[str]] = None
    platos_fuertes: Optional[List[str]] = None
    guarniciones: Optional[List[str]] = None
    bebidas: Optional[List[str]] = None
    postres: Optional[List[str]] = None
    comidas_corridas: Optional[List[Dict[str, Any]]] = None

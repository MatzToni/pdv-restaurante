from pydantic import BaseModel
from typing import Optional, List
from app.models.mesa import EstadoMesa

class AreaBase(BaseModel):
    nombre: str

class AreaCreate(AreaBase):
    pass

class AreaOut(AreaBase):
    id: int
    activo: bool

    class Config:
        from_attributes = True

class MesaBase(BaseModel):
    numero: str
    area_id: Optional[int] = None
    capacidad: int = 4
    estado: EstadoMesa = EstadoMesa.LIBRE

class MesaCreate(MesaBase):
    pass

class MesaUpdateEstado(BaseModel):
    estado: EstadoMesa

class MesaUpdateCapacidad(BaseModel):
    capacidad: int

class MesaUpdate(BaseModel):
    numero: Optional[str] = None
    area_id: Optional[int] = None
    capacidad: Optional[int] = None
    estado: Optional[EstadoMesa] = None
    activa: Optional[bool] = None

class MesaOut(MesaBase):
    id: int
    activa: bool
    area: Optional[AreaOut] = None

    class Config:
        from_attributes = True

from pydantic import BaseModel, EmailStr
from typing import Optional
from app.models.usuario import RolUsuario

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    rol: RolUsuario = RolUsuario.MESERO
    pin_seguridad: Optional[str] = None
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioOut(UsuarioBase):
    id: int

    class Config:
        from_attributes = True

class UsuarioAuthPIN(BaseModel):
    pin: str

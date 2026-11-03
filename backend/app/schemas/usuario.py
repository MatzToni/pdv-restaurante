from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.usuario import RolUsuario, TurnoTrabajo, TipoDocumentoPersonal

class DocumentoPersonalBase(BaseModel):
    tipo: TipoDocumentoPersonal = TipoDocumentoPersonal.OTRO
    titulo: str = Field(..., max_length=100)
    url_archivo: Optional[str] = Field(None, max_length=255)
    notas: Optional[str] = Field(None, max_length=255)
    fecha_vencimiento: Optional[date] = None

class DocumentoPersonalCreate(DocumentoPersonalBase):
    pass

class DocumentoPersonalOut(DocumentoPersonalBase):
    id: int
    usuario_id: int
    fecha_subida: datetime

    class Config:
        from_attributes = True

class UsuarioBase(BaseModel):
    nombre: str = Field(..., max_length=80)
    email: str = Field(..., max_length=100)
    rol: RolUsuario = RolUsuario.MESERO
    turno: TurnoTrabajo = TurnoTrabajo.MATUTINO
    acceso_sistema: bool = True
    activo: bool = True
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    curp: Optional[str] = Field(None, max_length=18)
    rfc: Optional[str] = Field(None, max_length=13)
    nss: Optional[str] = Field(None, max_length=15)
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=80)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=20)
    fecha_ingreso: Optional[date] = None
    salario_diario: Optional[Decimal] = Field(Decimal("0.0"), ge=0, le=99999.99)
    notas_expediente: Optional[str] = Field(None, max_length=500)

class UsuarioCreate(UsuarioBase):
    pin_seguridad: Optional[str] = Field(None, max_length=10)
    password: Optional[str] = Field("edencafe123", max_length=100)

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, max_length=80)
    email: Optional[str] = Field(None, max_length=100)
    rol: Optional[RolUsuario] = None
    turno: Optional[TurnoTrabajo] = None
    acceso_sistema: Optional[bool] = None
    pin_seguridad: Optional[str] = Field(None, max_length=10)
    password: Optional[str] = Field(None, max_length=100)
    activo: Optional[bool] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = Field(None, max_length=200)
    curp: Optional[str] = Field(None, max_length=18)
    rfc: Optional[str] = Field(None, max_length=13)
    nss: Optional[str] = Field(None, max_length=15)
    contacto_emergencia_nombre: Optional[str] = Field(None, max_length=80)
    contacto_emergencia_telefono: Optional[str] = Field(None, max_length=20)
    fecha_ingreso: Optional[date] = None
    salario_diario: Optional[Decimal] = Field(None, ge=0, le=99999.99)
    notas_expediente: Optional[str] = Field(None, max_length=500)

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime
    tiene_pin: bool = False

    class Config:
        from_attributes = True

class UsuarioDetalleOut(UsuarioOut):
    documentos: List[DocumentoPersonalOut] = []

    class Config:
        from_attributes = True

class UsuarioAuthPIN(BaseModel):
    pin: str

class UsuarioLoginPIN(BaseModel):
    pin: str
    usuario_id: Optional[int] = None

class UsuarioLoginPassword(BaseModel):
    email: str
    password: str

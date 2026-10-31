from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from app.models.usuario import RolUsuario, TurnoTrabajo, TipoDocumentoPersonal

class DocumentoPersonalBase(BaseModel):
    tipo: TipoDocumentoPersonal = TipoDocumentoPersonal.OTRO
    titulo: str
    url_archivo: Optional[str] = None
    notas: Optional[str] = None
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
    nombre: str
    email: str
    rol: RolUsuario = RolUsuario.MESERO
    turno: TurnoTrabajo = TurnoTrabajo.MATUTINO
    acceso_sistema: bool = True
    pin_seguridad: Optional[str] = None
    activo: bool = True
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    curp: Optional[str] = None
    rfc: Optional[str] = None
    nss: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    salario_diario: Optional[Decimal] = Decimal("0.0")
    notas_expediente: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: Optional[str] = "edencafe123"

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[str] = None
    rol: Optional[RolUsuario] = None
    turno: Optional[TurnoTrabajo] = None
    acceso_sistema: Optional[bool] = None
    pin_seguridad: Optional[str] = None
    activo: Optional[bool] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    curp: Optional[str] = None
    rfc: Optional[str] = None
    nss: Optional[str] = None
    contacto_emergencia_nombre: Optional[str] = None
    contacto_emergencia_telefono: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    salario_diario: Optional[Decimal] = None
    notas_expediente: Optional[str] = None

class UsuarioOut(UsuarioBase):
    id: int
    fecha_creacion: datetime

    class Config:
        from_attributes = True

class UsuarioDetalleOut(UsuarioOut):
    documentos: List[DocumentoPersonalOut] = []

    class Config:
        from_attributes = True

class UsuarioAuthPIN(BaseModel):
    pin: str

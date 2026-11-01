import enum
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Numeric, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class RolUsuario(str, enum.Enum):
    ADMINISTRADOR = "administrador"
    GERENTE = "gerente"
    JEFE = "jefe"
    COCINA = "cocina"
    MESERO = "mesero"
    AUXILIAR_GENERAL = "auxiliar_general"

class TurnoTrabajo(str, enum.Enum):
    MATUTINO = "matutino"       # Ej. 7:00 a 15:00
    VESPERTINO = "vespertino"   # Ej. 15:00 a 23:00
    NOCTURNO = "nocturno"
    COMPLETO = "completo"
    MIXTO = "mixto"

class TipoDocumentoPersonal(str, enum.Enum):
    IDENTIFICACION_INE = "identificacion_ine"
    RFC = "rfc"
    CURP = "curp"
    NSS_SEGURO = "nss_seguro"
    CONTRATO_LABORAL = "contrato_laboral"
    CERTIFICADO_SALUD = "certificado_salud"
    COMPROBANTE_DOMICILIO = "comprobante_domicilio"
    OTRO = "otro"

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(Enum(RolUsuario), nullable=False, default=RolUsuario.MESERO)
    turno = Column(Enum(TurnoTrabajo), nullable=False, default=TurnoTrabajo.MATUTINO)
    acceso_sistema = Column(Boolean, default=True, nullable=False) # Si tiene permiso para iniciar sesión en la terminal
    pin_seguridad = Column(String(10), nullable=True) # PIN de 4 dígitos para autorizaciones rápidas
    activo = Column(Boolean, default=True, nullable=False)

    # Datos Personales y Expediente Laboral
    telefono = Column(String(20), nullable=True)
    direccion = Column(Text, nullable=True)
    curp = Column(String(25), nullable=True)
    rfc = Column(String(20), nullable=True)
    nss = Column(String(25), nullable=True)
    contacto_emergencia_nombre = Column(String(100), nullable=True)
    contacto_emergencia_telefono = Column(String(20), nullable=True)
    fecha_ingreso = Column(Date, nullable=True)
    salario_diario = Column(Numeric(10, 2), default=0.0, nullable=True)
    notas_expediente = Column(Text, nullable=True)
    fecha_creacion = Column(DateTime(timezone=True), server_default=func.now())

    # Documentos del Personal
    documentos = relationship("DocumentoPersonal", back_populates="usuario", cascade="all, delete-orphan")

    @property
    def tiene_pin(self) -> bool:
        return bool(self.pin_seguridad)

class DocumentoPersonal(Base):
    __tablename__ = "documentos_personal"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    tipo = Column(Enum(TipoDocumentoPersonal), nullable=False, default=TipoDocumentoPersonal.OTRO)
    titulo = Column(String(150), nullable=False)
    url_archivo = Column(String(255), nullable=True) # Ruta o enlace al archivo guardado
    notas = Column(Text, nullable=True)
    fecha_vencimiento = Column(Date, nullable=True) # Ej. vigencia de certificado médico o contrato
    fecha_subida = Column(DateTime(timezone=True), server_default=func.now())

    usuario = relationship("Usuario", back_populates="documentos")

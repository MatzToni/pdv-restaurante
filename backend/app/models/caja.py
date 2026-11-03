import enum
from sqlalchemy import Column, Integer, Numeric, Boolean, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class EstadoCaja(str, enum.Enum):
    ABIERTA = "abierta"
    CERRADA = "cerrada"

class MetodoPago(str, enum.Enum):
    EFECTIVO = "efectivo"
    TARJETA = "tarjeta"
    TRANSFERENCIA = "transferencia"

class CajaTurno(Base):
    __tablename__ = "caja_turnos"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    monto_apertura = Column(Numeric(10, 2), default=0.0, nullable=False)
    fecha_apertura = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)
    monto_cierre_declarado = Column(Numeric(10, 2), nullable=True) # Lo que cuenta el cajero
    monto_cierre_sistema = Column(Numeric(10, 2), nullable=True)   # Lo que el sistema calculó
    estado = Column(Enum(EstadoCaja), default=EstadoCaja.ABIERTA, nullable=False)
    notas = Column(Text, nullable=True)

    usuario = relationship("Usuario")
    pagos = relationship("Pago", back_populates="caja_turno")

    @property
    def usuario_nombre(self):
        return self.usuario.nombre if self.usuario else None

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    caja_turno_id = Column(Integer, ForeignKey("caja_turnos.id"), nullable=True)
    monto = Column(Numeric(10, 2), nullable=False)
    metodo = Column(Enum(MetodoPago), nullable=False, default=MetodoPago.EFECTIVO)
    propina = Column(Numeric(10, 2), default=0.0, nullable=False)
    cambio = Column(Numeric(10, 2), default=0.0, nullable=False)
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    orden = relationship("Orden", back_populates="pagos")
    caja_turno = relationship("CajaTurno", back_populates="pagos")

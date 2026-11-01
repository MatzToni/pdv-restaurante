import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class EstadoMesa(str, enum.Enum):
    LIBRE = "libre"
    OCUPADA = "ocupada"
    CUENTA = "cuenta"
    RESERVADA = "reservada"

class Area(Base):
    __tablename__ = "areas"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False) # ej. Salón Principal, Terraza, Barra
    activo = Column(Boolean, default=True, nullable=False)

    mesas = relationship("Mesa", back_populates="area", cascade="all, delete-orphan")

class Mesa(Base):
    __tablename__ = "mesas"

    id = Column(Integer, primary_key=True, index=True)
    numero = Column(String(100), unique=True, nullable=False) # ej. Mesa 1, Terraza 3, Barra 2
    area_id = Column(Integer, ForeignKey("areas.id"), nullable=True)
    mesero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True) # Mesero asignado a la mesa
    capacidad = Column(Integer, default=4, nullable=True)
    estado = Column(Enum(EstadoMesa), default=EstadoMesa.LIBRE, nullable=False)
    activa = Column(Boolean, default=True, nullable=False)

    area = relationship("Area", back_populates="mesas")
    mesero = relationship("Usuario")
    ordenes = relationship("Orden", back_populates="mesa")

    @property
    def mesero_nombre(self):
        return self.mesero.nombre if self.mesero else None

import enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class EstadoOrden(str, enum.Enum):
    EN_COLA = "en_cola"
    PREPARANDO = "preparando"
    LISTO = "listo"
    ENTREGADO = "entregado"
    PAGADO = "pagado"
    CANCELADA = "cancelada"

class EstadoOrdenItem(str, enum.Enum):
    PENDIENTE = "pendiente"
    PREPARANDO = "preparando"
    LISTO = "listo"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=False)
    mesero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado = Column(Enum(EstadoOrden), default=EstadoOrden.EN_COLA, nullable=False)
    notas = Column(Text, nullable=True)
    subtotal = Column(Numeric(10, 2), default=0.0, nullable=False)
    descuento = Column(Numeric(10, 2), default=0.0, nullable=False)
    total = Column(Numeric(10, 2), default=0.0, nullable=False)
    fecha_apertura = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    fecha_cierre = Column(DateTime(timezone=True), nullable=True)

    mesa = relationship("Mesa", back_populates="ordenes")
    mesero = relationship("Usuario")
    items = relationship("OrdenItem", back_populates="orden", cascade="all, delete-orphan")
    pagos = relationship("Pago", back_populates="orden")

class OrdenItem(Base):
    __tablename__ = "orden_items"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    notas = Column(String(255), nullable=True) # ej. "Término 3/4, sin cebolla"
    estado = Column(Enum(EstadoOrdenItem), default=EstadoOrdenItem.PENDIENTE, nullable=False)
    
    # Manejo de rechazos y cancelaciones
    usuario_cancelo_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    motivo_cancelacion = Column(String(255), nullable=True)
    genera_merma = Column(Boolean, default=False, nullable=False) # True si ya se preparó la comida

    orden = relationship("Orden", back_populates="items")
    producto = relationship("Producto")
    usuario_cancelo = relationship("Usuario")

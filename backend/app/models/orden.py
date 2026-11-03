import enum
from typing import Optional
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum, ForeignKey, DateTime, Text, JSON
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
    EN_OBSERVACION = "en_observacion"
    LISTO = "listo"
    RECIBIDO_MESERO = "recibido_mesero"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"

class Orden(Base):
    __tablename__ = "ordenes"

    id = Column(Integer, primary_key=True, index=True)
    mesa_id = Column(Integer, ForeignKey("mesas.id"), nullable=True)
    mesero_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)
    estado = Column(Enum(EstadoOrden), default=EstadoOrden.EN_COLA, nullable=False)
    tipo_pedido = Column(String(30), default="comedor", nullable=False) # comedor, para_llevar, domicilio
    costo_envio = Column(Numeric(10, 2), default=0.0, nullable=False)
    datos_entrega = Column(JSON, nullable=True) # {"cliente": "...", "telefono": "...", "direccion": "...", "notas": "..."}
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

    @property
    def mesa_numero(self) -> str:
        if self.tipo_pedido == "domicilio":
            cli = (self.datos_entrega or {}).get("cliente", "")
            return f"🛵 Envío {f'- {cli}' if cli else f'#{self.id}'}"
        elif self.tipo_pedido == "para_llevar":
            cli = (self.datos_entrega or {}).get("cliente", "")
            return f"🛍️ Mostrador {f'- {cli}' if cli else f'#{self.id}'}"
        return self.mesa.numero if self.mesa else f"Mesa {self.mesa_id or 'S/M'}"

    @property
    def mesa_estado(self) -> Optional[str]:
        if self.mesa and self.mesa.estado:
            return self.mesa.estado.value if hasattr(self.mesa.estado, "value") else str(self.mesa.estado)
        return None

    @property
    def mesero_nombre(self) -> str:
        if self.tipo_pedido == "comedor" and self.mesa and self.mesa.mesero:
            return self.mesa.mesero.nombre
        if self.tipo_pedido in ["domicilio", "para_llevar"] and not self.mesa_id:
            return f"{self.mesero.nombre} (Mostrador)" if self.mesero else "Mostrador / Caja"
        return self.mesero.nombre if self.mesero else f"Mesero #{self.mesero_id}"

class OrdenItem(Base):
    __tablename__ = "orden_items"

    id = Column(Integer, primary_key=True, index=True)
    orden_id = Column(Integer, ForeignKey("ordenes.id"), nullable=False)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    cantidad = Column(Integer, default=1, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=False)
    notas = Column(String(255), nullable=True) # ej. "Término 3/4, sin cebolla"
    extras = Column(JSON, default=list, nullable=True) # [{"nombre": "Extra queso", "precio": 20.0}]
    observacion_cocina = Column(String(255), nullable=True) # Aclaración o falta de ingrediente desde cocina
    estado = Column(Enum(EstadoOrdenItem), default=EstadoOrdenItem.PENDIENTE, nullable=False)
    para_llevar = Column(Boolean, default=False, nullable=False) # Si el producto se pide para llevar / empaque desechable
    cargo_desechable = Column(Numeric(10, 2), default=0.0, nullable=False)
    
    # Manejo de rechazos y cancelaciones
    usuario_cancelo_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    motivo_cancelacion = Column(String(255), nullable=True)
    genera_merma = Column(Boolean, default=False, nullable=False) # True si ya se preparó la comida

    orden = relationship("Orden", back_populates="items")
    producto = relationship("Producto")
    usuario_cancelo = relationship("Usuario")

    @property
    def producto_nombre(self) -> str:
        return self.producto.nombre if self.producto else f"Platillo #{self.producto_id}"

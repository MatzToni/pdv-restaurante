import enum
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Enum, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base

class TipoArticulo(str, enum.Enum):
    INGREDIENTE = "ingrediente" # Carne, verdura, fruta, café, condimentos
    DESECHABLE = "desechable"   # Vasos, servilletas, popotes, bolsas
    UTENSILIO = "utensilio"     # Platos, coladores, tazas, cubiertos
    LIMPIEZA = "limpieza"       # Escobas, detergentes, sanitizantes

class TipoMovimientoInventario(str, enum.Enum):
    ENTRADA = "entrada"
    SALIDA_VENTA = "salida_venta"
    MERMA_DESPERDICIO = "merma_desperdicio"
    AJUSTE = "ajuste"

class ArticuloInventario(Base):
    __tablename__ = "articulos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String(50), unique=True, nullable=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoArticulo), nullable=False, default=TipoArticulo.INGREDIENTE)
    unidad_medida = Column(String(20), nullable=False) # kg, g, lt, ml, pza, paquete
    stock_actual = Column(Numeric(12, 3), default=0.0, nullable=False)
    stock_minimo = Column(Numeric(12, 3), default=0.0, nullable=False)
    costo_unitario = Column(Numeric(10, 2), default=0.0, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)

    recetas = relationship("Receta", back_populates="articulo")
    movimientos = relationship("MovimientoInventario", back_populates="articulo")

class Receta(Base):
    __tablename__ = "recetas"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("productos.id"), nullable=False)
    articulo_id = Column(Integer, ForeignKey("articulos_inventario.id"), nullable=False)
    cantidad_requerida = Column(Numeric(10, 3), nullable=False) # ej. 0.200 kg para una hamburguesa

    producto = relationship("Producto", back_populates="receta_items")
    articulo = relationship("ArticuloInventario", back_populates="recetas")

class MovimientoInventario(Base):
    __tablename__ = "movimientos_inventario"

    id = Column(Integer, primary_key=True, index=True)
    articulo_id = Column(Integer, ForeignKey("articulos_inventario.id"), nullable=False)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    tipo = Column(Enum(TipoMovimientoInventario), nullable=False)
    cantidad = Column(Numeric(12, 3), nullable=False)
    stock_resultante = Column(Numeric(12, 3), nullable=False)
    motivo = Column(Text, nullable=True) # ej. "Merma por platillo cancelado", "Recepción de compra"
    fecha = Column(DateTime(timezone=True), server_default=func.now())

    articulo = relationship("ArticuloInventario", back_populates="movimientos")
    usuario = relationship("Usuario")

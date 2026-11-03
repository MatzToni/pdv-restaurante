from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.session import Base

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False) # ej. Cafetería, Desayunos, Platos Fuertes
    descripcion = Column(Text, nullable=True)
    orden = Column(Integer, default=0)
    activo = Column(Boolean, default=True, nullable=False)

    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")

class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, index=True)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)
    nombre = Column(String(100), nullable=False)
    tipo_item = Column(String(30), default="platillo", nullable=True) # platillo, bebida, producto, servicio, menu_del_dia
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    disponible = Column(Boolean, default=True, nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    requiere_cocina = Column(Boolean, default=True, nullable=False) # Si no requiere cocina (ej. refresco en lata)

    categoria = relationship("Categoria", back_populates="productos")
    receta_items = relationship("Receta", back_populates="producto", cascade="all, delete-orphan")

    @property
    def categoria_nombre(self) -> str:
        return self.categoria.nombre if self.categoria else ""

class MenuDelDiaConfig(Base):
    __tablename__ = "menu_del_dia_config"

    id = Column(Integer, primary_key=True, default=1)
    activo = Column(Boolean, default=True, nullable=False)
    nombre = Column(String(100), default="Menú del Día (Comida Corrida)", nullable=False)
    descripcion = Column(Text, default="Comida corrida completa: Entrada, Plato Fuerte con guarnición, Bebida y Postre casero", nullable=True)
    precio = Column(Numeric(10, 2), default=95.0, nullable=False)
    hora_inicio = Column(String(5), default="12:00", nullable=False)
    hora_fin = Column(String(5), default="18:00", nullable=False)
    entradas = Column(JSON, default=list, nullable=False)
    platos_fuertes = Column(JSON, default=list, nullable=False)
    guarniciones = Column(JSON, default=list, nullable=False)
    bebidas = Column(JSON, default=list, nullable=False)
    postres = Column(JSON, default=list, nullable=False)
    comidas_corridas = Column(JSON, default=list, nullable=True)

from sqlalchemy import Column, Integer, String, Text, Numeric, Boolean, ForeignKey
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
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    imagen_url = Column(String(255), nullable=True)
    disponible = Column(Boolean, default=True, nullable=False)
    requiere_cocina = Column(Boolean, default=True, nullable=False) # Si no requiere cocina (ej. refresco en lata)

    categoria = relationship("Categoria", back_populates="productos")
    receta_items = relationship("Receta", back_populates="producto", cascade="all, delete-orphan")

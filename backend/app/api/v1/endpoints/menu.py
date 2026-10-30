from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.menu import Categoria, Producto
from app.models.inventario import Receta
from app.schemas.menu import CategoriaOut, CategoriaCreate, ProductoOut, ProductoCreate

router = APIRouter()

@router.get("/categorias", response_model=List[CategoriaOut], summary="Listar categorías del menú")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).filter(Categoria.activo == True).order_by(Categoria.orden).all()

@router.post("/categorias", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED, summary="Crear categoría")
def crear_categoria(cat_in: CategoriaCreate, db: Session = Depends(get_db)):
    nueva = Categoria(nombre=cat_in.nombre, descripcion=cat_in.descripcion, orden=cat_in.orden)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.get("/productos", response_model=List[ProductoOut], summary="Listar productos del menú")
def listar_productos(categoria_id: int = None, db: Session = Depends(get_db)):
    query = db.query(Producto).filter(Producto.disponible == True)
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    return query.all()

@router.post("/productos", response_model=ProductoOut, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo platillo o bebida con receta")
def crear_producto(prod_in: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_prod = Producto(
        categoria_id=prod_in.categoria_id,
        nombre=prod_in.nombre,
        descripcion=prod_in.descripcion,
        precio=prod_in.precio,
        disponible=prod_in.disponible,
        requiere_cocina=prod_in.requiere_cocina,
        imagen_url=prod_in.imagen_url
    )
    db.add(nuevo_prod)
    db.commit()
    db.refresh(nuevo_prod)

    # Si incluye insumos/receta
    if prod_in.receta:
        for r in prod_in.receta:
            item_receta = Receta(
                producto_id=nuevo_prod.id,
                articulo_id=r.articulo_id,
                cantidad_requerida=r.cantidad_requerida
            )
            db.add(item_receta)
        db.commit()
        db.refresh(nuevo_prod)

    return nuevo_prod

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.db.session import get_db
from app.models.menu import Categoria, Producto
from app.models.inventario import Receta
from app.schemas.menu import (
    CategoriaOut,
    CategoriaCreate,
    CategoriaUpdate,
    ProductoOut,
    ProductoCreate,
    ProductoUpdate
)

router = APIRouter()

# --- CATEGORÍAS (Tipo o Género) ---

@router.get("/categorias", response_model=List[CategoriaOut], summary="Listar categorías del menú")
def listar_categorias(db: Session = Depends(get_db)):
    return db.query(Categoria).filter(Categoria.activo == True).order_by(Categoria.orden).all()

@router.post("/categorias", response_model=CategoriaOut, status_code=status.HTTP_201_CREATED, summary="Crear categoría (tipo o género)")
def crear_categoria(cat_in: CategoriaCreate, db: Session = Depends(get_db)):
    existente = db.query(Categoria).filter(Categoria.nombre == cat_in.nombre).first()
    if existente:
        if not existente.activo:
            existente.activo = True
            existente.descripcion = cat_in.descripcion
            existente.orden = cat_in.orden
            db.commit()
            db.refresh(existente)
            return existente
        raise HTTPException(status_code=400, detail="Ya existe una categoría con ese nombre.")

    nueva = Categoria(nombre=cat_in.nombre, descripcion=cat_in.descripcion, orden=cat_in.orden)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@router.put("/categorias/{categoria_id}", response_model=CategoriaOut, summary="Actualizar categoría")
def actualizar_categoria(categoria_id: int, cat_in: CategoriaUpdate, db: Session = Depends(get_db)):
    cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    if cat_in.nombre is not None:
        cat.nombre = cat_in.nombre
    if cat_in.descripcion is not None:
        cat.descripcion = cat_in.descripcion
    if cat_in.orden is not None:
        cat.orden = cat_in.orden
    if cat_in.activo is not None:
        cat.activo = cat_in.activo

    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/categorias/{categoria_id}", summary="Eliminar / Desactivar categoría")
def eliminar_categoria(categoria_id: int, db: Session = Depends(get_db)):
    cat = db.query(Categoria).filter(Categoria.id == categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada.")

    # Desactivar
    cat.activo = False
    db.commit()
    return {"message": "Categoría desactivada correctamente"}


# --- PRODUCTOS, PLATILLOS Y SERVICIOS ---

@router.get("/productos", response_model=List[ProductoOut], summary="Listar productos del menú")
def listar_productos(
    categoria_id: Optional[int] = None, 
    incluir_inactivos: bool = False,
    db: Session = Depends(get_db)
):
    query = db.query(Producto).options(joinedload(Producto.categoria))
    if not incluir_inactivos:
        query = query.filter(Producto.disponible == True)
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    return query.order_by(Producto.nombre.asc()).all()

@router.post("/productos", response_model=ProductoOut, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo platillo, producto o servicio")
def crear_producto(prod_in: ProductoCreate, db: Session = Depends(get_db)):
    cat = db.query(Categoria).filter(Categoria.id == prod_in.categoria_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="La categoría especificada no existe.")

    nuevo_prod = Producto(
        categoria_id=prod_in.categoria_id,
        nombre=prod_in.nombre,
        tipo_item=prod_in.tipo_item or "platillo",
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

@router.put("/productos/{producto_id}", response_model=ProductoOut, summary="Actualizar platillo, producto o servicio")
def actualizar_producto(producto_id: int, prod_in: ProductoUpdate, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Platillo o producto no encontrado.")

    if prod_in.categoria_id is not None:
        cat = db.query(Categoria).filter(Categoria.id == prod_in.categoria_id).first()
        if not cat:
            raise HTTPException(status_code=404, detail="Categoría no encontrada.")
        prod.categoria_id = prod_in.categoria_id

    if prod_in.nombre is not None:
        prod.nombre = prod_in.nombre
    if prod_in.tipo_item is not None:
        prod.tipo_item = prod_in.tipo_item
    if prod_in.descripcion is not None:
        prod.descripcion = prod_in.descripcion
    if prod_in.precio is not None:
        prod.precio = prod_in.precio
    if prod_in.disponible is not None:
        prod.disponible = prod_in.disponible
    if prod_in.requiere_cocina is not None:
        prod.requiere_cocina = prod_in.requiere_cocina
    if prod_in.imagen_url is not None:
        prod.imagen_url = prod_in.imagen_url

    db.commit()
    db.refresh(prod)
    return prod

@router.patch("/productos/{producto_id}/disponibilidad", response_model=ProductoOut, summary="Alternar disponibilidad de platillo")
def alternar_disponibilidad(producto_id: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Platillo no encontrado.")

    prod.disponible = not prod.disponible
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/productos/{producto_id}", summary="Eliminar platillo o producto")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    prod = db.query(Producto).filter(Producto.id == producto_id).first()
    if not prod:
        raise HTTPException(status_code=404, detail="Platillo no encontrado.")

    # Marcar como no disponible en lugar de romper llaves foráneas de órdenes pasadas
    prod.disponible = False
    db.commit()
    return {"message": "Platillo desactivado correctamente"}

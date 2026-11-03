import os
import shutil
import uuid
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from app.core.config import settings
from app.db.session import get_db
from app.models.menu import Categoria, Producto, MenuDelDiaConfig
from app.models.inventario import Receta
from app.models.orden import OrdenItem
from app.schemas.menu import (
    CategoriaOut,
    CategoriaCreate,
    CategoriaUpdate,
    ProductoOut,
    ProductoCreate,
    ProductoUpdate,
    MenuDelDiaConfigOut,
    MenuDelDiaConfigUpdate
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
    query = db.query(Producto).options(joinedload(Producto.categoria)).filter(Producto.activo == True)
    if not incluir_inactivos:
        query = query.filter(Producto.disponible == True)
    if categoria_id:
        query = query.filter(Producto.categoria_id == categoria_id)
    return query.order_by(Producto.nombre.asc()).all()

@router.post("/productos/subir-imagen", summary="Subir imagen de platillo, producto o servicio")
def subir_imagen_producto(file: UploadFile = File(...)):
    # Validar extensión de imagen
    extension = os.path.splitext(file.filename)[1].lower() if file.filename else ""
    if extension not in [".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"]:
        raise HTTPException(
            status_code=400,
            detail="Formato no soportado. Por favor sube un archivo de imagen válido (JPG, PNG, WEBP, GIF, SVG)."
        )

    os.makedirs(settings.UPLOADS_DIR, exist_ok=True)

    nombre_archivo = f"dish_{uuid.uuid4().hex[:12]}{extension}"
    ruta_destino = os.path.join(settings.UPLOADS_DIR, nombre_archivo)

    with open(ruta_destino, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "url": f"/uploads/{nombre_archivo}",
        "nombre_archivo": nombre_archivo
    }

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

    # Verificar si tiene registros históricos en órdenes
    tiene_ordenes = db.query(OrdenItem).filter(OrdenItem.producto_id == producto_id).first()
    if tiene_ordenes:
        # Desactivar lógicamente para no romper claves foráneas de ventas pasadas
        prod.activo = False
        prod.disponible = False
        db.commit()
        return {"message": "Platillo archivado y retirado del catálogo general."}
    else:
        # Eliminación física directa de la base de datos
        db.delete(prod)
        db.commit()
        return {"message": "Platillo eliminado definitivamente del catálogo general."}

# --- CONFIGURACIÓN Y GESTIÓN DEL MENÚ DEL DÍA (COMIDA CORRIDA) ---

@router.get("/menu-del-dia", response_model=MenuDelDiaConfigOut, summary="Obtener configuración del Menú del Día de hoy")
def obtener_menu_del_dia(db: Session = Depends(get_db)):
    config = db.query(MenuDelDiaConfig).first()
    if not config:
        config = MenuDelDiaConfig(
            id=1,
            activo=True,
            nombre="Menú del Día (Comida Corrida)",
            descripcion="Comida corrida completa con Entrada, Plato Fuerte, Guarnición, Bebida y Postre casero",
            precio=Decimal("95.00"),
            hora_inicio="12:00",
            hora_fin="18:00",
            entradas=["Sopa de fideo casera", "Consomé de pollo con verduras", "Crema del día"],
            platos_fuertes=["Milanesa empanizada de pollo o res", "Mojarra frita al mojo de ajo", "Albóndigas caseras en chipotle", "Pechuga asada a la plancha"],
            guarniciones=["Arroz mexicano y frijoles refritos", "Papas a la francesa y ensalada fresca"],
            bebidas=["Agua fresca de Jamaica", "Agua de Limón con pepino y chía", "Agua de Guayaba"],
            postres=["Gelatina de mosaico", "Arroz con leche", "Flan napolitano", "Sin postre"],
            comidas_corridas=[
                {
                    "id": "1",
                    "nombre": "Comida Corrida 1: Milanesa de pollo con espagueti verde",
                    "precio": 95.0,
                    "activo": True,
                    "entradas": ["Sopa"],
                    "platos_fuertes": ["Milanesa de pollo con espagueti verde"],
                    "bebidas": ["Agua de jamaica"],
                    "postres": []
                },
                {
                    "id": "2",
                    "nombre": "Comida Corrida 2: Albóndigas con arroz rojo",
                    "precio": 95.0,
                    "activo": True,
                    "entradas": ["Puchero"],
                    "platos_fuertes": ["Albóndiga con arroz rojo"],
                    "bebidas": ["Agua de limón con pepino"],
                    "postres": ["Gelatina"]
                }
            ]
        )
        db.add(config)
        db.commit()
        db.refresh(config)
    
    # Asegurar que comidas_corridas tenga al menos los ejemplos por defecto si está vacío
    if not config.comidas_corridas:
        config.comidas_corridas = [
            {
                "id": "1",
                "nombre": "Comida Corrida 1: Milanesa de pollo con espagueti verde",
                "precio": float(config.precio or 95.0),
                "activo": True,
                "entradas": ["Sopa"],
                "platos_fuertes": ["Milanesa de pollo con espagueti verde"],
                "bebidas": ["Agua de jamaica"],
                "postres": []
            },
            {
                "id": "2",
                "nombre": "Comida Corrida 2: Albóndigas con arroz rojo",
                "precio": float(config.precio or 95.0),
                "activo": True,
                "entradas": ["Puchero"],
                "platos_fuertes": ["Albóndiga con arroz rojo"],
                "bebidas": ["Agua de limón con pepino"],
                "postres": ["Gelatina"]
            }
        ]
        db.commit()
        db.refresh(config)

    return config

@router.put("/menu-del-dia", response_model=MenuDelDiaConfigOut, summary="Actualizar opciones y horario del Menú del Día")
def actualizar_menu_del_dia(config_in: MenuDelDiaConfigUpdate, db: Session = Depends(get_db)):
    config = db.query(MenuDelDiaConfig).first()
    if not config:
        config = MenuDelDiaConfig(id=1)
        db.add(config)

    if config_in.activo is not None:
        config.activo = config_in.activo
    if config_in.nombre is not None:
        config.nombre = config_in.nombre
    if config_in.descripcion is not None:
        config.descripcion = config_in.descripcion
    if config_in.precio is not None:
        config.precio = config_in.precio
    if config_in.hora_inicio is not None:
        config.hora_inicio = config_in.hora_inicio
    if config_in.hora_fin is not None:
        config.hora_fin = config_in.hora_fin
    if config_in.entradas is not None:
        config.entradas = config_in.entradas
    if config_in.platos_fuertes is not None:
        config.platos_fuertes = config_in.platos_fuertes
    if config_in.guarniciones is not None:
        config.guarniciones = config_in.guarniciones
    if config_in.bebidas is not None:
        config.bebidas = config_in.bebidas
    if config_in.postres is not None:
        config.postres = config_in.postres
    if config_in.comidas_corridas is not None:
        config.comidas_corridas = config_in.comidas_corridas

    # Sincronizar existencia de producto "menu_del_dia" en el catálogo
    prod = db.query(Producto).filter(Producto.tipo_item == "menu_del_dia").first()
    if not prod:
        cat = db.query(Categoria).filter(Categoria.nombre.ilike("%platillo%")).first() or db.query(Categoria).first()
        if cat:
            prod = Producto(
                categoria_id=cat.id,
                nombre=config.nombre,
                tipo_item="menu_del_dia",
                descripcion=config.descripcion,
                precio=config.precio,
                disponible=config.activo,
                requiere_cocina=True
            )
            db.add(prod)
    elif prod:
        prod.nombre = config.nombre
        prod.descripcion = config.descripcion
        prod.precio = config.precio
        prod.disponible = config.activo

    db.commit()
    db.refresh(config)
    return config

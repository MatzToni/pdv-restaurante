from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal
from app.db.session import get_db
from app.models.inventario import ArticuloInventario, MovimientoInventario, TipoArticulo, TipoMovimientoInventario
from app.schemas.inventario import (
    ArticuloInventarioOut,
    ArticuloInventarioCreate,
    MovimientoInventarioOut,
    MovimientoInventarioCreate
)

router = APIRouter()

@router.get("/articulos", response_model=List[ArticuloInventarioOut], summary="Listar inventario clasificado por tipos")
def listar_inventario(tipo: Optional[TipoArticulo] = None, db: Session = Depends(get_db)):
    query = db.query(ArticuloInventario).filter(ArticuloInventario.activo == True)
    if tipo:
        query = query.filter(ArticuloInventario.tipo == tipo)
    return query.order_by(ArticuloInventario.tipo, ArticuloInventario.nombre).all()

@router.post("/articulos", response_model=ArticuloInventarioOut, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo artículo en inventario")
def crear_articulo(art_in: ArticuloInventarioCreate, db: Session = Depends(get_db)):
    nuevo = ArticuloInventario(
        codigo=art_in.codigo,
        nombre=art_in.nombre,
        tipo=art_in.tipo,
        unidad_medida=art_in.unidad_medida,
        stock_actual=art_in.stock_actual,
        stock_minimo=art_in.stock_minimo,
        costo_unitario=art_in.costo_unitario
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    # Si entra con stock inicial > 0, registrar movimiento inicial
    if art_in.stock_actual > 0:
        mov = MovimientoInventario(
            articulo_id=nuevo.id,
            tipo=TipoMovimientoInventario.ENTRADA,
            cantidad=art_in.stock_actual,
            stock_resultante=art_in.stock_actual,
            motivo="Carga de stock inicial"
        )
        db.add(mov)
        db.commit()

    return nuevo

@router.post("/movimientos", response_model=MovimientoInventarioOut, status_code=status.HTTP_201_CREATED, summary="Registrar movimiento (entrada, salida, merma, ajuste)")
def registrar_movimiento(mov_in: MovimientoInventarioCreate, db: Session = Depends(get_db)):
    articulo = db.query(ArticuloInventario).filter(ArticuloInventario.id == mov_in.articulo_id).first()
    if not articulo:
        raise HTTPException(status_code=404, detail="Artículo no encontrado en el inventario.")

    # Calcular stock resultante según el tipo
    if mov_in.tipo == TipoMovimientoInventario.ENTRADA:
        nuevo_stock = articulo.stock_actual + mov_in.cantidad
    elif mov_in.tipo in [TipoMovimientoInventario.SALIDA_VENTA, TipoMovimientoInventario.MERMA_DESPERDICIO]:
        nuevo_stock = max(Decimal("0.0"), articulo.stock_actual - mov_in.cantidad)
    elif mov_in.tipo == TipoMovimientoInventario.AJUSTE:
        nuevo_stock = mov_in.cantidad
    else:
        nuevo_stock = articulo.stock_actual

    articulo.stock_actual = nuevo_stock

    movimiento = MovimientoInventario(
        articulo_id=articulo.id,
        tipo=mov_in.tipo,
        cantidad=mov_in.cantidad,
        stock_resultante=nuevo_stock,
        motivo=mov_in.motivo
    )
    db.add(movimiento)
    db.commit()
    db.refresh(movimiento)
    return movimiento

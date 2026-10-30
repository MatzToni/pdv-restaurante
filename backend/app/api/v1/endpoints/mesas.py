from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.mesa import Mesa, Area, EstadoMesa
from app.schemas.mesa import MesaOut, MesaCreate, MesaUpdateEstado, AreaOut, AreaCreate

router = APIRouter()

@router.get("/areas", response_model=List[AreaOut], summary="Listar áreas del restaurante")
def listar_areas(db: Session = Depends(get_db)):
    return db.query(Area).filter(Area.activo == True).all()

@router.post("/areas", response_model=AreaOut, status_code=status.HTTP_201_CREATED, summary="Crear nueva área")
def crear_area(area_in: AreaCreate, db: Session = Depends(get_db)):
    nueva_area = Area(nombre=area_in.nombre)
    db.add(nueva_area)
    db.commit()
    db.refresh(nueva_area)
    return nueva_area

@router.get("/", response_model=List[MesaOut], summary="Listar todas las mesas activas")
def listar_mesas(db: Session = Depends(get_db)):
    return db.query(Mesa).filter(Mesa.activa == True).order_by(Mesa.id).all()

@router.post("/", response_model=MesaOut, status_code=status.HTTP_201_CREATED, summary="Crear una nueva mesa")
def crear_mesa(mesa_in: MesaCreate, db: Session = Depends(get_db)):
    existente = db.query(Mesa).filter(Mesa.numero == mesa_in.numero).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una mesa con esa denominación.")
    
    nueva_mesa = Mesa(
        numero=mesa_in.numero,
        area_id=mesa_in.area_id,
        capacidad=mesa_in.capacidad,
        estado=mesa_in.estado
    )
    db.add(nueva_mesa)
    db.commit()
    db.refresh(nueva_mesa)
    return nueva_mesa

@router.patch("/{mesa_id}/estado", response_model=MesaOut, summary="Actualizar estado de una mesa")
def actualizar_estado_mesa(mesa_id: int, estado_in: MesaUpdateEstado, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")
    mesa.estado = estado_in.estado
    db.commit()
    db.refresh(mesa)
    return mesa

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.mesa import Mesa, Area, EstadoMesa
from app.schemas.mesa import MesaOut, MesaCreate, MesaUpdateEstado, MesaUpdateCapacidad, MesaUpdate, AreaOut, AreaCreate

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

@router.patch("/{mesa_id}/capacidad", response_model=MesaOut, summary="Actualizar capacidad de una mesa")
def actualizar_capacidad_mesa(mesa_id: int, cap_in: MesaUpdateCapacidad, db: Session = Depends(get_db)):
    if cap_in.capacidad < 1:
        raise HTTPException(status_code=400, detail="La capacidad debe ser de al menos 1 persona.")
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")
    mesa.capacidad = cap_in.capacidad
    db.commit()
    db.refresh(mesa)
    return mesa

@router.patch("/{mesa_id}", response_model=MesaOut, summary="Actualizar datos de una mesa")
def actualizar_mesa(mesa_id: int, mesa_in: MesaUpdate, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")
    
    if mesa_in.numero is not None and mesa_in.numero != mesa.numero:
        existente = db.query(Mesa).filter(Mesa.numero == mesa_in.numero, Mesa.id != mesa_id).first()
        if existente:
            raise HTTPException(status_code=400, detail="Ya existe una mesa con esa denominación.")
        mesa.numero = mesa_in.numero
        
    if mesa_in.area_id is not None:
        if mesa_in.area_id > 0:
            area = db.query(Area).filter(Area.id == mesa_in.area_id, Area.activo == True).first()
            if not area:
                raise HTTPException(status_code=404, detail="Área no encontrada.")
            mesa.area_id = mesa_in.area_id
        else:
            mesa.area_id = None

    if mesa_in.capacidad is not None:
        if mesa_in.capacidad < 1:
            raise HTTPException(status_code=400, detail="La capacidad debe ser de al menos 1 persona.")
        mesa.capacidad = mesa_in.capacidad

    if mesa_in.estado is not None:
        mesa.estado = mesa_in.estado

    if mesa_in.activa is not None:
        mesa.activa = mesa_in.activa

    db.commit()
    db.refresh(mesa)
    return mesa

@router.delete("/{mesa_id}", status_code=status.HTTP_200_OK, summary="Eliminar o desactivar una mesa")
def eliminar_mesa(mesa_id: int, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")
    if mesa.estado != EstadoMesa.LIBRE:
        raise HTTPException(status_code=400, detail="No se puede eliminar una mesa que no está libre.")
    mesa.activa = False
    db.commit()
    return {"mensaje": f"Mesa {mesa.numero} eliminada exitosamente"}

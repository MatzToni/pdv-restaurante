from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from app.db.session import get_db
from app.models.mesa import Mesa, Area, EstadoMesa
from app.models.orden import Orden, EstadoOrden, EstadoOrdenItem
from app.models.usuario import Usuario, RolUsuario
from app.schemas.mesa import (
    MesaOut,
    MesaCreate,
    MesaUpdateEstado,
    MesaUpdateCapacidad,
    MesaAsignarMesero,
    MesaUpdate,
    AreaOut,
    AreaCreate
)

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
    return db.query(Mesa).options(
        joinedload(Mesa.mesero),
        joinedload(Mesa.area),
        joinedload(Mesa.ordenes).joinedload(Orden.items)
    ).filter(Mesa.activa == True).order_by(Mesa.id).all()

@router.post("/", response_model=MesaOut, status_code=status.HTTP_201_CREATED, summary="Crear una nueva mesa")
def crear_mesa(mesa_in: MesaCreate, db: Session = Depends(get_db)):
    existente = db.query(Mesa).filter(Mesa.numero == mesa_in.numero).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe una mesa con esa denominación.")
    
    if mesa_in.mesero_id is not None:
        mesero = db.query(Usuario).filter(Usuario.id == mesa_in.mesero_id, Usuario.activo == True).first()
        if not mesero:
            raise HTTPException(status_code=404, detail="Colaborador no encontrado o inactivo.")
        if mesero.rol not in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL, RolUsuario.ADMINISTRADOR]:
            raise HTTPException(status_code=400, detail="Solo los meseros y auxiliares generales pueden tener asignadas mesas para atender.")

    nueva_mesa = Mesa(
        numero=mesa_in.numero,
        area_id=mesa_in.area_id,
        mesero_id=mesa_in.mesero_id,
        capacidad=mesa_in.capacidad or 4,
        estado=mesa_in.estado or EstadoMesa.LIBRE
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
    if estado_in.estado == EstadoMesa.CUENTA:
        # Validar que exista al menos una orden activa con productos no cancelados
        orden_activa = db.query(Orden).filter(
            Orden.mesa_id == mesa_id,
            Orden.estado.in_([EstadoOrden.EN_COLA, EstadoOrden.PREPARANDO, EstadoOrden.LISTO, EstadoOrden.ENTREGADO])
        ).first()
        if not orden_activa or not any(i.estado != EstadoOrdenItem.CANCELADO for i in orden_activa.items):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede solicitar la cuenta de una mesa sin pedidos o servicios realizados."
            )
    if estado_in.estado == EstadoMesa.LIBRE:
        mesa.mesero_id = None
    mesa.estado = estado_in.estado
    db.commit()
    db.refresh(mesa)
    return mesa

@router.patch("/{mesa_id}/mesero", response_model=MesaOut, summary="Asignar o desasignar mesero a una mesa")
def asignar_mesero_mesa(mesa_id: int, datos: MesaAsignarMesero, db: Session = Depends(get_db)):
    mesa = db.query(Mesa).filter(Mesa.id == mesa_id).first()
    if not mesa:
        raise HTTPException(status_code=404, detail="Mesa no encontrada.")
    if datos.mesero_id is not None:
        mesero = db.query(Usuario).filter(Usuario.id == datos.mesero_id, Usuario.activo == True).first()
        if not mesero:
            raise HTTPException(status_code=404, detail="Colaborador no encontrado o inactivo.")
        if mesero.rol not in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL, RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE]:
            raise HTTPException(
                status_code=400,
                detail="Solo los meseros, auxiliares y administración pueden tener asignadas mesas para atender."
            )
        mesa.mesero_id = datos.mesero_id
        if mesa.estado == EstadoMesa.LIBRE:
            mesa.estado = EstadoMesa.OCUPADA
    else:
        mesa.mesero_id = None
        if mesa.estado == EstadoMesa.OCUPADA and not mesa.tiene_consumo:
            mesa.estado = EstadoMesa.LIBRE
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

    if "mesero_id" in mesa_in.model_fields_set:
        if mesa_in.mesero_id is not None:
            mesero = db.query(Usuario).filter(Usuario.id == mesa_in.mesero_id, Usuario.activo == True).first()
            if not mesero:
                raise HTTPException(status_code=404, detail="Colaborador no encontrado o inactivo.")
            if mesero.rol not in [RolUsuario.MESERO, RolUsuario.AUXILIAR_GENERAL, RolUsuario.ADMINISTRADOR]:
                raise HTTPException(status_code=400, detail="Solo los meseros y auxiliares generales pueden tener asignadas mesas para atender.")
        mesa.mesero_id = mesa_in.mesero_id

    if mesa_in.estado is not None:
        if mesa_in.estado == EstadoMesa.LIBRE:
            mesa.mesero_id = None
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

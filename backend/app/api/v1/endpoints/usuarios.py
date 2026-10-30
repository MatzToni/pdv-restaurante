from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.models.usuario import Usuario, RolUsuario
from app.schemas.usuario import UsuarioOut, UsuarioCreate, UsuarioAuthPIN

router = APIRouter()

@router.get("/", response_model=List[UsuarioOut], summary="Listar todos los usuarios y personal")
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).filter(Usuario.activo == True).all()

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED, summary="Crear un nuevo usuario con rol")
def crear_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con este correo electrónico.")
    
    nuevo_usuario = Usuario(
        nombre=usuario_in.nombre,
        email=usuario_in.email,
        password_hash=usuario_in.password, # Para producción usar hash
        rol=usuario_in.rol,
        pin_seguridad=usuario_in.pin_seguridad,
        activo=usuario_in.activo
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.post("/verificar-pin", summary="Verificar PIN de autorización para cancelaciones o descuentos")
def verificar_pin(auth: UsuarioAuthPIN, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.pin_seguridad == auth.pin,
        Usuario.activo == True,
        Usuario.rol.in_([RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE])
    ).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="PIN inválido o usuario sin permisos de autorización.")
    return {"valido": True, "autorizado_por": usuario.nombre, "rol": usuario.rol}

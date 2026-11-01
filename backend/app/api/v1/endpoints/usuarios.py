from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models.usuario import Usuario, RolUsuario, TurnoTrabajo, DocumentoPersonal
from app.schemas.usuario import (
    UsuarioOut,
    UsuarioDetalleOut,
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioAuthPIN,
    UsuarioLoginPIN,
    UsuarioLoginPassword,
    DocumentoPersonalOut,
    DocumentoPersonalCreate
)

router = APIRouter()

@router.get("/", response_model=List[UsuarioOut], summary="Listar todos los colaboradores del personal")
def listar_usuarios(
    turno: Optional[TurnoTrabajo] = None,
    solo_con_acceso: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Usuario).filter(Usuario.activo == True)
    if turno:
        query = query.filter(Usuario.turno == turno)
    if solo_con_acceso is not None:
        query = query.filter(Usuario.acceso_sistema == solo_con_acceso)
    return query.order_by(Usuario.id).all()

@router.get("/{usuario_id}", response_model=UsuarioDetalleOut, summary="Obtener detalle completo de un colaborador con su expediente y documentos")
def obtener_detalle_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado.")
    return usuario

@router.post("/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED, summary="Registrar nuevo personal")
def crear_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if existente:
        raise HTTPException(status_code=400, detail="Ya existe un colaborador con este correo electrónico.")
    
    if usuario_in.pin_seguridad:
        pin_str = str(usuario_in.pin_seguridad).strip()
        if pin_str and (not pin_str.isdigit() or len(pin_str) != 4):
            raise HTTPException(status_code=400, detail="El PIN de seguridad debe contener exactamente 4 dígitos numéricos.")

    nuevo_usuario = Usuario(
        nombre=usuario_in.nombre,
        email=usuario_in.email,
        password_hash=usuario_in.password or "edencafe123",
        rol=usuario_in.rol,
        turno=usuario_in.turno,
        acceso_sistema=usuario_in.acceso_sistema,
        pin_seguridad=usuario_in.pin_seguridad,
        activo=usuario_in.activo,
        telefono=usuario_in.telefono,
        direccion=usuario_in.direccion,
        curp=usuario_in.curp,
        rfc=usuario_in.rfc,
        nss=usuario_in.nss,
        contacto_emergencia_nombre=usuario_in.contacto_emergencia_nombre,
        contacto_emergencia_telefono=usuario_in.contacto_emergencia_telefono,
        fecha_ingreso=usuario_in.fecha_ingreso,
        salario_diario=usuario_in.salario_diario,
        notas_expediente=usuario_in.notas_expediente
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@router.put("/{usuario_id}", response_model=UsuarioDetalleOut, summary="Actualizar información o expediente del colaborador")
@router.patch("/{usuario_id}", response_model=UsuarioDetalleOut, summary="Actualizar información o expediente del colaborador")
def actualizar_usuario(usuario_id: int, datos: UsuarioUpdate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado.")

    if datos.pin_seguridad is not None:
        pin_str = str(datos.pin_seguridad).strip()
        if pin_str and (not pin_str.isdigit() or len(pin_str) != 4):
            raise HTTPException(status_code=400, detail="El PIN de seguridad debe contener exactamente 4 dígitos numéricos.")

    datos_dict = datos.model_dump(exclude_unset=True)
    for campo, valor in datos_dict.items():
        setattr(usuario, campo, valor)

    db.commit()
    db.refresh(usuario)
    return usuario

@router.post("/{usuario_id}/documentos", response_model=DocumentoPersonalOut, status_code=status.HTTP_201_CREATED, summary="Registrar un documento en el expediente del colaborador")
def agregar_documento_personal(usuario_id: int, doc_in: DocumentoPersonalCreate, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Colaborador no encontrado.")

    nuevo_doc = DocumentoPersonal(
        usuario_id=usuario_id,
        tipo=doc_in.tipo,
        titulo=doc_in.titulo,
        url_archivo=doc_in.url_archivo,
        notas=doc_in.notas,
        fecha_vencimiento=doc_in.fecha_vencimiento
    )
    db.add(nuevo_doc)
    db.commit()
    db.refresh(nuevo_doc)
    return nuevo_doc

@router.delete("/documentos/{documento_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar documento del expediente")
def eliminar_documento(documento_id: int, db: Session = Depends(get_db)):
    doc = db.query(DocumentoPersonal).filter(DocumentoPersonal.id == documento_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Documento no encontrado.")
    db.delete(doc)
    db.commit()
    return None

@router.post("/verificar-pin", summary="Verificar PIN de autorización para cancelaciones o descuentos")
def verificar_pin(auth: UsuarioAuthPIN, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(
        Usuario.pin_seguridad == auth.pin,
        Usuario.activo == True,
        Usuario.acceso_sistema == True,
        Usuario.rol.in_([RolUsuario.ADMINISTRADOR, RolUsuario.GERENTE, RolUsuario.JEFE])
    ).first()
    if not usuario:
        raise HTTPException(status_code=403, detail="PIN inválido o usuario sin permisos de autorización.")
    return {"valido": True, "autorizado_por": usuario.nombre, "rol": usuario.rol}

@router.post("/login-pin", response_model=UsuarioOut, summary="Iniciar sesión validando PIN de 4 dígitos")
def login_pin(credenciales: UsuarioLoginPIN, db: Session = Depends(get_db)):
    pin_limpio = str(credenciales.pin).strip()
    if not pin_limpio.isdigit() or len(pin_limpio) != 4:
        raise HTTPException(status_code=400, detail="El PIN debe contener exactamente 4 dígitos numéricos.")

    query = db.query(Usuario).filter(
        Usuario.activo == True,
        Usuario.acceso_sistema == True
    )
    if credenciales.usuario_id is not None:
        usuario = query.filter(Usuario.id == credenciales.usuario_id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Colaborador no encontrado.")
        if usuario.pin_seguridad != pin_limpio:
            raise HTTPException(status_code=401, detail="PIN incorrecto para este perfil.")
    else:
        usuario = query.filter(Usuario.pin_seguridad == pin_limpio).first()
        if not usuario:
            raise HTTPException(status_code=401, detail="PIN no reconocido o colaborador sin acceso.")

    return usuario

@router.post("/login-password", response_model=UsuarioOut, summary="Iniciar sesión con correo y contraseña")
def login_password(credenciales: UsuarioLoginPassword, db: Session = Depends(get_db)):
    email_limpio = credenciales.email.strip().lower()
    usuario = db.query(Usuario).filter(
        Usuario.email.ilike(email_limpio),
        Usuario.activo == True,
        Usuario.acceso_sistema == True
    ).first()
    if not usuario or usuario.password_hash != credenciales.password:
        raise HTTPException(status_code=401, detail="Correo electrónico o contraseña incorrectos.")
    return usuario

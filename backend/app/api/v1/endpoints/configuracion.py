from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.configuracion import ConfiguracionSistema
from app.schemas.configuracion import ConfiguracionOut, ConfiguracionUpdate

router = APIRouter()

def _obtener_o_crear_config(db: Session) -> ConfiguracionSistema:
    cfg = db.query(ConfiguracionSistema).first()
    if not cfg:
        cfg = ConfiguracionSistema(id=1)
        db.add(cfg)
        db.commit()
        db.refresh(cfg)
    return cfg

@router.get("/", response_model=ConfiguracionOut, summary="Obtener configuración central del sistema")
def obtener_configuracion(db: Session = Depends(get_db)):
    return _obtener_o_crear_config(db)

@router.put("/", response_model=ConfiguracionOut, summary="Actualizar configuración central del sistema")
def actualizar_configuracion(datos: ConfiguracionUpdate, db: Session = Depends(get_db)):
    cfg = _obtener_o_crear_config(db)
    
    update_data = datos.model_dump(exclude_unset=True)
    for field, val in update_data.items():
        if hasattr(cfg, field) and val is not None:
            setattr(cfg, field, val)

    db.commit()
    db.refresh(cfg)
    return cfg

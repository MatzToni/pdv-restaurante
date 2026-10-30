from fastapi import APIRouter
from app.api.v1.endpoints import health, usuarios, mesas, menu, inventario, ordenes

api_router = APIRouter()

api_router.include_router(health.router, tags=["Salud del Sistema"])
api_router.include_router(usuarios.router, prefix="/usuarios", tags=["Gestión de Usuarios y Roles"])
api_router.include_router(mesas.router, prefix="/mesas", tags=["Control de Mesas y Áreas"])
api_router.include_router(menu.router, prefix="/menu", tags=["Catálogo de Platillos y Menú"])
api_router.include_router(inventario.router, prefix="/inventario", tags=["Inventario y Materia Prima"])
api_router.include_router(ordenes.router, prefix="/ordenes", tags=["Comandas y Cancelaciones"])

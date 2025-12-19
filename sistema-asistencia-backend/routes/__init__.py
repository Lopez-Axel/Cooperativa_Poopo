from fastapi import APIRouter
from .auth import router as auth_router
from .devices import router as devices_router
from .users import router as users_router
from .secciones import router as secciones_router
from .cuadrillas import router as cuadrillas_router
from .cooperativistas import router as cooperativistas_router
from .attendance import router as attendance_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(devices_router)
api_router.include_router(users_router)
api_router.include_router(secciones_router)
api_router.include_router(cuadrillas_router)
api_router.include_router(cooperativistas_router)
api_router.include_router(attendance_router)

__all__ = ["api_router"]
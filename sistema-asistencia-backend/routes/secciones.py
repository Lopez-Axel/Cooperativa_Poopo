from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from utils.dependencies import get_db, get_current_user
from services.seccion_service import seccion_service
from schemas.seccion import SeccionCreate, SeccionUpdate, SeccionResponse, SeccionWithDelegadoResponse

router = APIRouter(prefix="/secciones", tags=["Secciones"])

@router.post("/", response_model=SeccionResponse)
def create_seccion(
    seccion_data: SeccionCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.create_seccion(db, seccion_data, current_user.id)

@router.get("/", response_model=List[SeccionResponse])
def get_secciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.get_all(db, skip, limit)

@router.get("/active", response_model=List[SeccionResponse])
def get_active_secciones(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.get_active(db)

@router.get("/{seccion_id}", response_model=SeccionResponse)
def get_seccion(
    seccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.get_by_id(db, seccion_id)

@router.get("/{seccion_id}/delegado", response_model=SeccionWithDelegadoResponse)
def get_seccion_with_delegado(
    seccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.get_by_id_with_delegado(db, seccion_id)

@router.put("/{seccion_id}", response_model=SeccionResponse)
def update_seccion(
    seccion_id: int,
    seccion_data: SeccionUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.update_seccion(db, seccion_id, seccion_data)

@router.delete("/{seccion_id}")
def delete_seccion(
    seccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return seccion_service.delete_seccion(db, seccion_id)
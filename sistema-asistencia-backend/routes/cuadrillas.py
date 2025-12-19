from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from utils.dependencies import get_db, get_current_user
from services.cuadrilla_service import cuadrilla_service
from schemas.cuadrilla import CuadrillaCreate, CuadrillaUpdate, CuadrillaResponse, CuadrillaDetailsResponse


router = APIRouter(prefix="/cuadrillas", tags=["Cuadrillas"])

@router.post("/", response_model=CuadrillaResponse)
def create_cuadrilla(
    cuadrilla_data: CuadrillaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.create_cuadrilla(db, cuadrilla_data, current_user.id)

@router.get("/", response_model=List[CuadrillaResponse])
def get_cuadrillas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.get_all(db, skip, limit)

@router.get("/active", response_model=List[CuadrillaResponse])
def get_active_cuadrillas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.get_active(db)

@router.get("/seccion/{seccion_id}", response_model=List[CuadrillaResponse])
def get_cuadrillas_by_seccion(
    seccion_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.get_by_seccion(db, seccion_id)

@router.get("/{cuadrilla_id}", response_model=CuadrillaResponse)
def get_cuadrilla(
    cuadrilla_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.get_by_id(db, cuadrilla_id)

@router.put("/{cuadrilla_id}", response_model=CuadrillaResponse)
def update_cuadrilla(
    cuadrilla_id: int,
    cuadrilla_data: CuadrillaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.update_cuadrilla(db, cuadrilla_id, cuadrilla_data)

@router.delete("/{cuadrilla_id}")
def delete_cuadrilla(
    cuadrilla_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.delete_cuadrilla(db, cuadrilla_id)

@router.get("/{cuadrilla_id}/details", response_model=CuadrillaDetailsResponse)
def get_cuadrilla_details(
    cuadrilla_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cuadrilla_service.get_cuadrilla_details(db, cuadrilla_id)
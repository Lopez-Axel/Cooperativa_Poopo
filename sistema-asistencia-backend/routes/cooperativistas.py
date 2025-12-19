from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from utils.dependencies import get_db, get_current_user, get_current_superuser
from services.cooperativista_service import cooperativista_service
from schemas.cooperativista import CooperativistaCreate, CooperativistaUpdate, CooperativistaResponse

router = APIRouter(prefix="/cooperativistas", tags=["Cooperativistas"])

@router.post("/", response_model=CooperativistaResponse)
def create_cooperativista(
    cooperativista_data: CooperativistaCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.create_cooperativista(db, cooperativista_data, current_user.id)

@router.get("/", response_model=List[CooperativistaResponse])
def get_cooperativistas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.get_all(db, skip, limit)

@router.get("/active", response_model=List[CooperativistaResponse])
def get_active_cooperativistas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.get_active(db)

@router.get("/search", response_model=List[CooperativistaResponse])
def search_cooperativistas(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.search(db, q)

@router.get("/qr/{qr_code}", response_model=CooperativistaResponse)
def get_cooperativista_by_qr(
    qr_code: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.get_by_qr(db, qr_code)

@router.get("/{cooperativista_id}", response_model=CooperativistaResponse)
def get_cooperativista(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.get_by_id(db, cooperativista_id)

@router.put("/{cooperativista_id}", response_model=CooperativistaResponse)
def update_cooperativista(
    cooperativista_id: int,
    cooperativista_data: CooperativistaUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.update_cooperativista(db, cooperativista_id, cooperativista_data)

@router.delete("/{cooperativista_id}")
def delete_cooperativista(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return cooperativista_service.delete_cooperativista(db, cooperativista_id)

@router.post("/bulk/activate")
def activate_all_cooperativistas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    return cooperativista_service.activate_all(db)

@router.post("/bulk/deactivate")
def deactivate_all_cooperativistas(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_superuser)
):
    return cooperativista_service.deactivate_all(db)
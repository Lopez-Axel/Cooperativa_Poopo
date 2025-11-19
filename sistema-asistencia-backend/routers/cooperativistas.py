# routers/cooperativistas.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.cooperativista import Cooperativista
from schemas.cooperativista import CooperativistaCreate, CooperativistaUpdate, CooperativistaResponse
import secrets
import string

router = APIRouter(prefix="/cooperativistas", tags=["cooperativistas"])

def generar_codigo_unico(db: Session):
    while True:
        codigo = f"COOP-{''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(5))}"
        existe = db.query(Cooperativista).filter(Cooperativista.codigo_unico == codigo).first()
        if not existe:
            return codigo

@router.get("/", response_model=List[CooperativistaResponse])
def get_cooperativistas(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = None,
    cuadrilla: Optional[str] = None,
    seccion: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Cooperativista)
    
    if is_active is not None:
        query = query.filter(Cooperativista.is_active == is_active)
    if cuadrilla:
        query = query.filter(Cooperativista.cuadrilla.ilike(f"%{cuadrilla}%"))
    if seccion:
        query = query.filter(Cooperativista.seccion == seccion)
    if search:
        query = query.filter(
            (Cooperativista.nombres.ilike(f"%{search}%")) |
            (Cooperativista.apellido_paterno.ilike(f"%{search}%")) |
            (Cooperativista.apellido_materno.ilike(f"%{search}%")) |
            (Cooperativista.ci.ilike(f"%{search}%")) |
            (Cooperativista.codigo_unico.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/{cooperativista_id}", response_model=CooperativistaResponse)
def get_cooperativista(cooperativista_id: int, db: Session = Depends(get_db)):
    coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    return coop

@router.get("/codigo/{codigo_unico}", response_model=CooperativistaResponse)
def get_cooperativista_by_codigo(codigo_unico: str, db: Session = Depends(get_db)):
    coop = db.query(Cooperativista).filter(Cooperativista.codigo_unico == codigo_unico).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    return coop

@router.post("/", response_model=CooperativistaResponse, status_code=status.HTTP_201_CREATED)
def create_cooperativista(cooperativista: CooperativistaCreate, db: Session = Depends(get_db)):
    if db.query(Cooperativista).filter(Cooperativista.codigo_unico == cooperativista.codigo_unico).first():
        raise HTTPException(status_code=400, detail="El código único ya existe")
    
    if cooperativista.ci:
        existe_ci = db.query(Cooperativista).filter(Cooperativista.ci == cooperativista.ci).first()
        if existe_ci:
            raise HTTPException(status_code=400, detail="El CI ya está registrado")
    
    db_coop = Cooperativista(**cooperativista.model_dump())
    db.add(db_coop)
    db.commit()
    db.refresh(db_coop)
    return db_coop

@router.put("/{cooperativista_id}", response_model=CooperativistaResponse)
def update_cooperativista(
    cooperativista_id: int,
    cooperativista: CooperativistaUpdate,
    db: Session = Depends(get_db)
):
    db_coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not db_coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    update_data = cooperativista.model_dump(exclude_unset=True)
    
    if "codigo_unico" in update_data and update_data["codigo_unico"] != db_coop.codigo_unico:
        existe = db.query(Cooperativista).filter(
            Cooperativista.codigo_unico == update_data["codigo_unico"],
            Cooperativista.id != cooperativista_id
        ).first()
        if existe:
            raise HTTPException(status_code=400, detail="El código único ya existe")
    
    if "ci" in update_data and update_data["ci"]:
        existe_ci = db.query(Cooperativista).filter(
            Cooperativista.ci == update_data["ci"],
            Cooperativista.id != cooperativista_id
        ).first()
        if existe_ci:
            raise HTTPException(status_code=400, detail="El CI ya está registrado")
    
    for key, value in update_data.items():
        setattr(db_coop, key, value)
    
    db.commit()
    db.refresh(db_coop)
    return db_coop

@router.delete("/{cooperativista_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cooperativista(cooperativista_id: int, db: Session = Depends(get_db)):
    db_coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not db_coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    db.delete(db_coop)
    db.commit()
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.cooperativista_repo import cooperativista_repo
from models.cooperativista import Cooperativista
from schemas.cooperativista import CooperativistaCreate, CooperativistaUpdate, CooperativistaResponse
from core.qr_utils import generate_qr_code
from typing import List

class CooperativistaService:
    
    def create_cooperativista(self, db: Session, cooperativista_data: CooperativistaCreate, user_id: int) -> CooperativistaResponse:
        if cooperativista_data.ci:
            existing = cooperativista_repo.get_by_ci(db, cooperativista_data.ci)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CI ya registrado"
                )
        
        qr_code = generate_qr_code()
        while cooperativista_repo.get_by_qr_code(db, qr_code):
            qr_code = generate_qr_code()
        
        cooperativista = Cooperativista(
            **cooperativista_data.model_dump(),
            qr_code=qr_code,
            created_by=user_id
        )
        
        cooperativista = cooperativista_repo.create(db, cooperativista)
        return CooperativistaResponse.model_validate(cooperativista)
    
    def get_by_id(self, db: Session, cooperativista_id: int) -> CooperativistaResponse:
        cooperativista = cooperativista_repo.get_by_id(db, cooperativista_id)
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cooperativista no encontrado"
            )
        return CooperativistaResponse.model_validate(cooperativista)
    
    def get_by_qr(self, db: Session, qr_code: str) -> CooperativistaResponse:
        cooperativista = cooperativista_repo.get_by_qr_code(db, qr_code)
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR no válido"
            )
        return CooperativistaResponse.model_validate(cooperativista)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[CooperativistaResponse]:
        cooperativistas = cooperativista_repo.get_all(db, skip, limit)
        return [CooperativistaResponse.model_validate(c) for c in cooperativistas]
    
    def get_active(self, db: Session) -> List[CooperativistaResponse]:
        cooperativistas = cooperativista_repo.get_active(db)
        return [CooperativistaResponse.model_validate(c) for c in cooperativistas]
    
    def search(self, db: Session, term: str) -> List[CooperativistaResponse]:
        cooperativistas = cooperativista_repo.search(db, term)
        return [CooperativistaResponse.model_validate(c) for c in cooperativistas]
    
    def update_cooperativista(self, db: Session, cooperativista_id: int, cooperativista_data: CooperativistaUpdate) -> CooperativistaResponse:
        cooperativista = cooperativista_repo.get_by_id(db, cooperativista_id)
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cooperativista no encontrado"
            )
        
        if cooperativista_data.ci and cooperativista_data.ci != cooperativista.ci:
            existing = cooperativista_repo.get_by_ci(db, cooperativista_data.ci)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="CI ya registrado"
                )
        
        for field, value in cooperativista_data.model_dump(exclude_unset=True).items():
            setattr(cooperativista, field, value)
        
        cooperativista = cooperativista_repo.update(db, cooperativista)
        return CooperativistaResponse.model_validate(cooperativista)
    
    def delete_cooperativista(self, db: Session, cooperativista_id: int) -> dict:
        cooperativista = cooperativista_repo.get_by_id(db, cooperativista_id)
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cooperativista no encontrado"
            )
        
        cooperativista_repo.delete(db, cooperativista)
        return {"message": "Cooperativista eliminado"}
    
    def activate_all(self, db: Session) -> dict:
        count = db.query(Cooperativista).update({"is_active": True})
        db.commit()
        return {
            "message": "Cooperativistas activados",
            "total_affected": count
        }
    
    def deactivate_all(self, db: Session) -> dict:
        count = db.query(Cooperativista).update({"is_active": False})
        db.commit()
        return {
            "message": "Cooperativistas desactivados",
            "total_affected": count
        }

cooperativista_service = CooperativistaService()
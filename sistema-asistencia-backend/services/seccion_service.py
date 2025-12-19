from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.seccion_repo import seccion_repo
from repositories.cooperativista_repo import cooperativista_repo
from models.seccion import Seccion
from schemas.seccion import SeccionCreate, SeccionUpdate, SeccionResponse, SeccionWithDelegadoResponse
from typing import List

class SeccionService:
    
    def create_seccion(self, db: Session, seccion_data: SeccionCreate, user_id: int) -> SeccionResponse:
        if seccion_repo.get_by_nombre(db, seccion_data.nombre):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sección ya existe"
            )
        
        if seccion_data.id_delegado:
            delegado = cooperativista_repo.get_by_id(db, seccion_data.id_delegado)
            if not delegado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cooperativista delegado no encontrado"
                )
        
        seccion = Seccion(
            **seccion_data.model_dump(),
            created_by=user_id
        )
        
        seccion = seccion_repo.create(db, seccion)
        return SeccionResponse.model_validate(seccion)
    
    def get_by_id(self, db: Session, seccion_id: int) -> SeccionResponse:
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        return SeccionResponse.model_validate(seccion)
    
    def get_by_id_with_delegado(self, db: Session, seccion_id: int) -> SeccionWithDelegadoResponse:
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        return SeccionWithDelegadoResponse.model_validate(seccion)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[SeccionResponse]:
        secciones = seccion_repo.get_all(db, skip, limit)
        return [SeccionResponse.model_validate(s) for s in secciones]
    
    def get_active(self, db: Session) -> List[SeccionResponse]:
        secciones = seccion_repo.get_active(db)
        return [SeccionResponse.model_validate(s) for s in secciones]
    
    def update_seccion(self, db: Session, seccion_id: int, seccion_data: SeccionUpdate) -> SeccionResponse:
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        if seccion_data.nombre and seccion_data.nombre != seccion.nombre:
            if seccion_repo.get_by_nombre(db, seccion_data.nombre):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Sección ya existe"
                )
        
        if seccion_data.id_delegado:
            delegado = cooperativista_repo.get_by_id(db, seccion_data.id_delegado)
            if not delegado:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Cooperativista delegado no encontrado"
                )
        
        for field, value in seccion_data.model_dump(exclude_unset=True).items():
            setattr(seccion, field, value)
        
        seccion = seccion_repo.update(db, seccion)
        return SeccionResponse.model_validate(seccion)
    
    def delete_seccion(self, db: Session, seccion_id: int) -> dict:
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        seccion_repo.delete(db, seccion)
        return {"message": "Sección eliminada"}

seccion_service = SeccionService()
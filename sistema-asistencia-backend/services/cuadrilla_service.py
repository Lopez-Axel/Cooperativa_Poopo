from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.cuadrilla_repo import cuadrilla_repo
from repositories.seccion_repo import seccion_repo
from models.cuadrilla import Cuadrilla
from schemas.cuadrilla import CuadrillaCreate, CuadrillaUpdate, CuadrillaResponse
from typing import List
from schemas.cuadrilla import CuadrillaDetailsResponse, CooperativistaInfo, SeccionInfo
from models.cooperativista import Cooperativista

class CuadrillaService:
    
    def create_cuadrilla(self, db: Session, cuadrilla_data: CuadrillaCreate, user_id: int) -> CuadrillaResponse:
        if not seccion_repo.get_by_id(db, cuadrilla_data.id_seccion):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        cuadrilla = Cuadrilla(
            **cuadrilla_data.model_dump(),
            created_by=user_id
        )
        
        cuadrilla = cuadrilla_repo.create(db, cuadrilla)
        return CuadrillaResponse.model_validate(cuadrilla)
    
    def get_by_id(self, db: Session, cuadrilla_id: int) -> CuadrillaResponse:
        cuadrilla = cuadrilla_repo.get_by_id(db, cuadrilla_id)
        if not cuadrilla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuadrilla no encontrada"
            )
        return CuadrillaResponse.model_validate(cuadrilla)
    
    def get_by_seccion(self, db: Session, seccion_id: int) -> List[CuadrillaResponse]:
        cuadrillas = cuadrilla_repo.get_by_seccion(db, seccion_id)
        return [CuadrillaResponse.model_validate(c) for c in cuadrillas]
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 500) -> List[CuadrillaResponse]:
        cuadrillas = cuadrilla_repo.get_all(db, skip, limit)
        return [CuadrillaResponse.model_validate(c) for c in cuadrillas]
    
    def get_active(self, db: Session) -> List[CuadrillaResponse]:
        cuadrillas = cuadrilla_repo.get_active(db)
        return [CuadrillaResponse.model_validate(c) for c in cuadrillas]
    
    def update_cuadrilla(self, db: Session, cuadrilla_id: int, cuadrilla_data: CuadrillaUpdate) -> CuadrillaResponse:
        cuadrilla = cuadrilla_repo.get_by_id(db, cuadrilla_id)
        if not cuadrilla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuadrilla no encontrada"
            )
        
        if cuadrilla_data.id_seccion:
            if not seccion_repo.get_by_id(db, cuadrilla_data.id_seccion):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sección no encontrada"
                )
        
        for field, value in cuadrilla_data.model_dump(exclude_unset=True).items():
            setattr(cuadrilla, field, value)
        
        cuadrilla = cuadrilla_repo.update(db, cuadrilla)
        return CuadrillaResponse.model_validate(cuadrilla)
    
    def delete_cuadrilla(self, db: Session, cuadrilla_id: int) -> dict:
        cuadrilla = cuadrilla_repo.get_by_id(db, cuadrilla_id)
        if not cuadrilla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuadrilla no encontrada"
            )
        
        cuadrilla_repo.delete(db, cuadrilla)
        return {"message": "Cuadrilla eliminada"}
    
    def get_cuadrilla_details(self, db: Session, cuadrilla_id: int) -> CuadrillaDetailsResponse:
        cuadrilla = cuadrilla_repo.get_by_id(db, cuadrilla_id)
        if not cuadrilla:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cuadrilla no encontrada"
            )
        
        cooperativistas_query = (
            db.query(Cooperativista)
            .filter(Cooperativista.id_cuadrilla == cuadrilla_id)
            .all()
        )
        
        cooperativistas_info = [
            CooperativistaInfo(
                id=c.id,
                nombres=c.nombres,
                apellido_paterno=c.apellido_paterno,
                apellido_materno=c.apellido_materno,
                ci=c.ci,
                rol_cuadrilla=c.rol_cuadrilla
            )
            for c in cooperativistas_query
        ]
        
        return CuadrillaDetailsResponse(
            id=cuadrilla.id,
            nombre=cuadrilla.nombre,
            created_at=cuadrilla.created_at,
            updated_at=cuadrilla.updated_at,
            seccion=SeccionInfo(
                id=cuadrilla.seccion.id,
                nombre=cuadrilla.seccion.nombre
            ) if cuadrilla.seccion else None,
            cooperativistas=cooperativistas_info,
            total_cooperativistas=len(cooperativistas_info)
        )

cuadrilla_service = CuadrillaService()
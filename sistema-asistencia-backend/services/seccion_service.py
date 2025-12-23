from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.seccion_repo import seccion_repo
from repositories.cooperativista_repo import cooperativista_repo
from models.seccion import Seccion
from schemas.seccion import SeccionCreate, SeccionUpdate, SeccionResponse, SeccionWithDelegadoResponse
from typing import List
from sqlalchemy import func
from schemas.seccion import SeccionDetailsResponse, CuadrillaInfo, DelegadoInfo
from models.cuadrilla import Cuadrilla
from models.cooperativista import Cooperativista
from repositories.cuadrilla_repo import cuadrilla_repo
from schemas.cuadrilla import CuadrillaResponse


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
    
    def get_seccion_details(self, db: Session, seccion_id: int) -> SeccionDetailsResponse:
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )
        
        cuadrillas_query = (
            db.query(
                Cuadrilla.id,
                Cuadrilla.nombre,
                func.count(Cooperativista.id).label('total_cooperativistas')
            )
            .outerjoin(Cooperativista, Cuadrilla.id == Cooperativista.id_cuadrilla)
            .filter(Cuadrilla.id_seccion == seccion_id)
            .group_by(Cuadrilla.id, Cuadrilla.nombre)
            .all()
        )
        
        cuadrillas_info = [
            CuadrillaInfo(
                id=c.id,
                nombre=c.nombre,
                total_cooperativistas=c.total_cooperativistas
            )
            for c in cuadrillas_query
        ]
        
        total_cooperativistas = (
            db.query(func.count(Cooperativista.id))
            .filter(Cooperativista.id_seccion == seccion_id)
            .scalar()
        )
        
        return SeccionDetailsResponse(
            id=seccion.id,
            nombre=seccion.nombre,
            descripcion=seccion.descripcion,
            created_at=seccion.created_at,
            updated_at=seccion.updated_at,
            delegado=DelegadoInfo.model_validate(seccion.delegado) if seccion.delegado else None,
            cuadrillas=cuadrillas_info,
            total_cuadrillas=len(cuadrillas_info),
            total_cooperativistas=total_cooperativistas or 0
        )
    
    def create_default_cuadrilla(self, db: Session, seccion_id: int, user_id: int) -> CuadrillaResponse:
        # Validar que la sección exista
        seccion = seccion_repo.get_by_id(db, seccion_id)
        if not seccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sección no encontrada"
            )

        # Verificar si ya existe la cuadrilla "SIN CUADRILLA" en esta sección
        existing = (
            db.query(Cuadrilla)
            .filter(
                Cuadrilla.id_seccion == seccion_id,
                Cuadrilla.nombre == "SIN CUADRILLA"
            )
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La sección ya tiene una cuadrilla por defecto"
            )

        # Crear la cuadrilla por defecto
        cuadrilla = Cuadrilla(
            nombre="SIN CUADRILLA",
            id_seccion=seccion_id,
            is_active=True,
            created_by=user_id
        )

        cuadrilla = cuadrilla_repo.create(db, cuadrilla)
        return CuadrillaResponse.model_validate(cuadrilla)
    
    def create_default_cuadrillas_bulk(self, db: Session, user_id: int) -> dict:
        secciones = seccion_repo.get_active(db)
        
        created_count = 0
        skipped_count = 0
        errors = []
        
        for seccion in secciones:
            try:
                existing = (
                    db.query(Cuadrilla)
                    .filter(
                        Cuadrilla.id_seccion == seccion.id,
                        Cuadrilla.nombre == "SIN CUADRILLA"
                    )
                    .first()
                )
                
                if existing:
                    skipped_count += 1
                    continue
                
                cuadrilla = Cuadrilla(
                    nombre="SIN CUADRILLA",
                    id_seccion=seccion.id,
                    is_active=True,
                    created_by=user_id
                )
                
                cuadrilla_repo.create(db, cuadrilla)
                created_count += 1
                
            except Exception as e:
                errors.append({
                    "seccion_id": seccion.id,
                    "seccion_nombre": seccion.nombre,
                    "error": str(e)
                })
        
        return {
            "message": "Proceso completado",
            "total_secciones": len(secciones),
            "cuadrillas_creadas": created_count,
            "cuadrillas_existentes": skipped_count,
            "errores": errors
        }



seccion_service = SeccionService()
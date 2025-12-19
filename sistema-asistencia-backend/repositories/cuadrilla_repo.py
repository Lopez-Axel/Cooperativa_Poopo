from sqlalchemy.orm import Session
from models.cuadrilla import Cuadrilla
from typing import Optional, List

class CuadrillaRepository:
    
    def get_by_id(self, db: Session, cuadrilla_id: int) -> Optional[Cuadrilla]:
        return db.query(Cuadrilla).filter(Cuadrilla.id == cuadrilla_id).first()
    
    def get_by_nombre(self, db: Session, nombre: str) -> Optional[Cuadrilla]:
        return db.query(Cuadrilla).filter(Cuadrilla.nombre == nombre).first()
    
    def get_by_seccion(self, db: Session, seccion_id: int) -> List[Cuadrilla]:
        return db.query(Cuadrilla).filter(Cuadrilla.id_seccion == seccion_id).all()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Cuadrilla]:
        return db.query(Cuadrilla).offset(skip).limit(limit).all()
    
    def get_active(self, db: Session) -> List[Cuadrilla]:
        return db.query(Cuadrilla).filter(Cuadrilla.is_active == True).all()
    
    def create(self, db: Session, cuadrilla: Cuadrilla) -> Cuadrilla:
        db.add(cuadrilla)
        db.commit()
        db.refresh(cuadrilla)
        return cuadrilla
    
    def update(self, db: Session, cuadrilla: Cuadrilla) -> Cuadrilla:
        db.commit()
        db.refresh(cuadrilla)
        return cuadrilla
    
    def delete(self, db: Session, cuadrilla: Cuadrilla) -> None:
        db.delete(cuadrilla)
        db.commit()

cuadrilla_repo = CuadrillaRepository()
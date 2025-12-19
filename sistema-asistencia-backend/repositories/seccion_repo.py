from sqlalchemy.orm import Session
from models.seccion import Seccion
from typing import Optional, List

class SeccionRepository:
    
    def get_by_id(self, db: Session, seccion_id: int) -> Optional[Seccion]:
        return db.query(Seccion).filter(Seccion.id == seccion_id).first()
    
    def get_by_nombre(self, db: Session, nombre: str) -> Optional[Seccion]:
        return db.query(Seccion).filter(Seccion.nombre == nombre).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Seccion]:
        return db.query(Seccion).offset(skip).limit(limit).all()
    
    def get_active(self, db: Session) -> List[Seccion]:
        return db.query(Seccion).filter(Seccion.is_active == True).all()
    
    def create(self, db: Session, seccion: Seccion) -> Seccion:
        db.add(seccion)
        db.commit()
        db.refresh(seccion)
        return seccion
    
    def update(self, db: Session, seccion: Seccion) -> Seccion:
        db.commit()
        db.refresh(seccion)
        return seccion
    
    def delete(self, db: Session, seccion: Seccion) -> None:
        db.delete(seccion)
        db.commit()

seccion_repo = SeccionRepository()
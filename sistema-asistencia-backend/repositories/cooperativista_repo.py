from sqlalchemy.orm import Session
from models.cooperativista import Cooperativista
from typing import Optional, List

class CooperativistaRepository:
    
    def get_by_id(self, db: Session, cooperativista_id: int) -> Optional[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    
    def get_by_qr_code(self, db: Session, qr_code: str) -> Optional[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.qr_code == qr_code).first()
    
    def get_by_ci(self, db: Session, ci: str) -> Optional[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.ci == ci).first()
    
    def get_by_cuadrilla(self, db: Session, cuadrilla_id: int) -> List[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.id_cuadrilla == cuadrilla_id).all()
    
    def get_by_seccion(self, db: Session, seccion_id: int) -> List[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.id_seccion == seccion_id).all()
    
    def get_all(self, db: Session) -> List[Cooperativista]:
        return db.query(Cooperativista).all()
    
    def get_active(self, db: Session) -> List[Cooperativista]:
        return db.query(Cooperativista).filter(Cooperativista.is_active == True).all()
    
    def search(self, db: Session, term: str) -> List[Cooperativista]:
        search_term = f"%{term}%"
        return db.query(Cooperativista).filter(
            (Cooperativista.nombres.ilike(search_term)) |
            (Cooperativista.apellido_paterno.ilike(search_term)) |
            (Cooperativista.apellido_materno.ilike(search_term)) |
            (Cooperativista.ci.ilike(search_term))
        ).all()
    
    def create(self, db: Session, cooperativista: Cooperativista) -> Cooperativista:
        db.add(cooperativista)
        db.commit()
        db.refresh(cooperativista)
        return cooperativista
    
    def update(self, db: Session, cooperativista: Cooperativista) -> Cooperativista:
        db.commit()
        db.refresh(cooperativista)
        return cooperativista
    
    def delete(self, db: Session, cooperativista: Cooperativista) -> None:
        db.delete(cooperativista)
        db.commit()

cooperativista_repo = CooperativistaRepository()
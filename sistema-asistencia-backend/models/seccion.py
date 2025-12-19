from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Seccion(Base):
    __tablename__ = "secciones"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nombre = Column(String(150), nullable=False, unique=True, index=True)
    descripcion = Column(String(500))
    id_delegado = Column(Integer, ForeignKey("cooperativistas.id", ondelete="SET NULL"), nullable=True, index=True)
    
    is_active = Column(Boolean, default=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    delegado = relationship("Cooperativista", foreign_keys=[id_delegado])
    cuadrillas = relationship("Cuadrilla", back_populates="seccion")
    cooperativistas = relationship("Cooperativista", back_populates="seccion", foreign_keys="Cooperativista.id_seccion")
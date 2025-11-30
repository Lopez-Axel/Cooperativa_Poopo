from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Cooperativista(Base):
    __tablename__ = "cooperativistas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # ❌ ELIMINADO: codigo_unico
    
    nro = Column(Integer, unique=True, nullable=False, index=True)  # ← Ahora único
    seccion = Column(String(150))
    cuadrilla = Column(String(150), index=True)
    jefe_cuadrilla = Column(String(150))
    delegado_seccion = Column(String(150))
    
    apellido_paterno = Column(String(150), nullable=False, index=True)
    apellido_materno = Column(String(150), index=True)
    nombres = Column(String(150), nullable=False, index=True)
    
    ci = Column(String(50), index=True)
    ci_expedido = Column(String(10))
    ci_foto_url = Column(String(500))
    documento_abc_url = Column(String(500))
    
    fecha_ingreso = Column(Date)
    fecha_nacimiento = Column(Date)

    codigo_asegurado = Column(String(100))
    cua = Column(String(50))
    ocupacion = Column(String(150))
    estado_asegurado = Column(String(50))
    
    email = Column(String(150))
    
    is_active = Column(Boolean, default=True, index=True)
    motivo_baja = Column(Text)
    fecha_baja = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    devices = relationship("Device", back_populates="cooperativista", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="cooperativista", cascade="all, delete-orphan")
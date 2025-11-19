from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Cooperativista(Base):
    __tablename__ = "cooperativistas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # CÓDIGO ÚNICO GENERADO
    codigo_unico = Column(String(10), unique=True, nullable=False, index=True)
    
    # DATOS DEL EXCEL
    nro = Column(Integer)
    seccion = Column(String(100))
    cuadrilla = Column(String(100), index=True)
    jefe_cuadrilla = Column(String(100))
    delegado_seccion = Column(String(100))
    
    # NOMBRES (SEPARADOS)
    apellido_paterno = Column(String(100), nullable=False, index=True)
    apellido_materno = Column(String(100), index=True)
    nombres = Column(String(100), nullable=False, index=True)
    
    # IDENTIFICACIÓN
    ci = Column(String(20), index=True)
    ci_expedido = Column(String(5))
    
    # FECHAS
    fecha_ingreso = Column(Date)
    fecha_nacimiento = Column(Date)

    # DATOS LABORALES
    codigo_asegurado = Column(String(50))
    ocupacion = Column(String(100))
    estado_asegurado = Column(String(20))
    
    # ESTADO
    is_active = Column(Boolean, default=True, index=True)
    motivo_baja = Column(Text)
    fecha_baja = Column(Date)
    
    # AUDITORÍA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # RELACIONES
    devices = relationship("Device", back_populates="cooperativista", cascade="all, delete-orphan")
    attendances = relationship("Attendance", back_populates="cooperativista", cascade="all, delete-orphan")
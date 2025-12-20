from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base
class Cooperativista(Base):
    __tablename__ = "cooperativistas"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    qr_code = Column(String(100), unique=True, nullable=False, index=True)

    id_seccion = Column(
        Integer,
        ForeignKey("secciones.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    id_cuadrilla = Column(
        Integer,
        ForeignKey("cuadrillas.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    rol_cuadrilla = Column(String(150))
    
    apellido_paterno = Column(String(150), nullable=False, index=True)
    apellido_materno = Column(String(150), index=True)
    nombres = Column(String(150), nullable=False, index=True)
    
    ci = Column(String(50), unique=True, index=True)
    ci_expedido = Column(String(10))
    ci_foto_url = Column(String(500))
    documento_abc_url = Column(String(500))
    
    fecha_ingreso = Column(Date)
    fecha_nacimiento = Column(Date)
    username_gestora = Column(String(100), unique=True, index=True)
    password_gestora = Column(String(200))
    codigo_asegurado = Column(String(100))
    cua = Column(String(50))
    ocupacion = Column(String(150))
    estado_asegurado = Column(String(50))
    
    email = Column(String(150))
    telefono = Column(String(50))
    
    is_active = Column(Boolean, default=True, index=True)
    motivo_baja = Column(Text)
    fecha_baja = Column(Date)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
 
    seccion = relationship(
        "Seccion",
        back_populates="cooperativistas",
        foreign_keys=[id_seccion]
    )

    cuadrilla = relationship(
        "Cuadrilla",
        back_populates="cooperativistas"
    )

    attendances = relationship(
        "Attendance",
        back_populates="cooperativista",
        cascade="all, delete-orphan"
    )

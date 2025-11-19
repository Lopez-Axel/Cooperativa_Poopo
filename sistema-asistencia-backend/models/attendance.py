from sqlalchemy import Column, Integer, String, DateTime, Date, Time, ForeignKey, Text, Float, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # RELACIONES
    cooperativista_id = Column(Integer, ForeignKey("cooperativistas.id", ondelete="CASCADE"), nullable=False, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    ubicacion_id = Column(Integer, ForeignKey("ubicaciones.id"))
    
    # TIPO DE REGISTRO
    tipo = Column(String(10), nullable=False, index=True)
    
    # TIMESTAMP
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    fecha = Column(Date, nullable=False, index=True)
    hora = Column(Time, nullable=False)
    
    # GPS (OBLIGATORIO)
    location_lat = Column(Float, nullable=False)
    location_lon = Column(Float, nullable=False)
    distance_meters = Column(Integer)
    
    # EXTRAS
    photo_url = Column(String(255))
    notes = Column(Text)
    
    # AUDITORÍA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # CONSTRAINT
    __table_args__ = (
        CheckConstraint("tipo IN ('entrada', 'salida')", name="chk_tipo"),
    )
    
    # RELACIONES
    cooperativista = relationship("Cooperativista", back_populates="attendances")
    ubicacion = relationship("Ubicacion", back_populates="attendances")
    logs = relationship("AttendanceLog", back_populates="attendance", cascade="all, delete-orphan")


class AttendanceLog(Base):
    __tablename__ = "attendance_logs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id", ondelete="CASCADE"), nullable=False, index=True)
    action = Column(String(20), nullable=False)
    changed_by = Column(Integer, ForeignKey("users.id"))
    old_values = Column(Text)
    new_values = Column(Text)
    reason = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # RELACIONES
    attendance = relationship("Attendance", back_populates="logs")
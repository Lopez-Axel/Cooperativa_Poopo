from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, Time, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class AttendancePeriod(Base):
    __tablename__ = "attendance_periods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    
    mes = Column(Integer, nullable=False, index=True)
    anio = Column(Integer, nullable=False, index=True)
    fecha_asistencia = Column(Date, nullable=False, index=True)
    
    hora_inicio = Column(Time, nullable=False)
    hora_fin = Column(Time, nullable=False)
    
    is_active = Column(Boolean, default=True, index=True)
    is_open = Column(Boolean, default=True, index=True)
    
    total_expected = Column(Integer, default=0)
    total_marked = Column(Integer, default=0)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    closed_at = Column(DateTime(timezone=True))
    closed_by = Column(Integer, ForeignKey("users.id"))

    __table_args__ = (
        CheckConstraint("mes >= 1 AND mes <= 12", name="chk_mes_valido"),
        CheckConstraint("anio >= 2024", name="chk_anio_valido"),
    )
    
    attendances = relationship("Attendance", back_populates="period")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    cooperativista_id = Column(Integer, ForeignKey("cooperativistas.id", ondelete="CASCADE"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("attendance_periods.id", ondelete="SET NULL"), nullable=True, index=True)
    registered_by = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    tipo = Column(String(10), nullable=False, index=True, default="entrada")
    
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    fecha = Column(Date, nullable=False, index=True)
    hora = Column(Time, nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    cooperativista = relationship("Cooperativista", back_populates="attendances")
    period = relationship("AttendancePeriod", back_populates="attendances")
    registered_by_user = relationship("User", back_populates="attendances_registered", foreign_keys=[registered_by])
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
    
    attendance = relationship("Attendance", back_populates="logs")

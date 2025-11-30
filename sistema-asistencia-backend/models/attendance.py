from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, Date, Time, ForeignKey, Text, CheckConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base

class AttendancePeriod(Base):
    """
    Define períodos mensuales de asistencia con fechas y horarios específicos.
    Máximo 2 períodos activos por mes.
    """
    __tablename__ = "attendance_periods"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # IDENTIFICACIÓN DEL PERÍODO
    nombre = Column(String(100), nullable=False)  # Ej: "Primera quincena Enero 2025"
    descripcion = Column(Text)
    
    # FECHA DEL PERÍODO
    mes = Column(Integer, nullable=False, index=True)  # 1-12
    anio = Column(Integer, nullable=False, index=True)  # 2025, 2026, etc.
    fecha_asistencia = Column(Date, nullable=False, index=True)  # Día específico de asistencia
    
    # HORARIO
    hora_inicio = Column(Time, nullable=False)  # Hora desde que pueden marcar
    hora_fin = Column(Time, nullable=False)  # Hora límite para marcar
    
    # ESTADO
    is_active = Column(Boolean, default=True, index=True)
    is_open = Column(Boolean, default=False, index=True)  # Si está abierto para marcar
    
    # METADATA
    total_expected = Column(Integer, default=0)  # Total de cooperativistas esperados
    total_marked = Column(Integer, default=0)  # Total que ya marcaron
    
    # AUDITORÍA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    closed_at = Column(DateTime(timezone=True))
    closed_by = Column(Integer, ForeignKey("users.id"))
    
    # CONSTRAINTS
    __table_args__ = (
        CheckConstraint("mes >= 1 AND mes <= 12", name="chk_mes_valido"),
        CheckConstraint("anio >= 2024", name="chk_anio_valido"),
    )
    
    # RELACIONES
    attendances = relationship("Attendance", back_populates="period")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # RELACIONES
    cooperativista_id = Column(Integer, ForeignKey("cooperativistas.id", ondelete="CASCADE"), nullable=False, index=True)
    period_id = Column(Integer, ForeignKey("attendance_periods.id", ondelete="SET NULL"), nullable=True, index=True)
    device_id = Column(String(255), nullable=False, index=True)
    # TIPO DE REGISTRO (mantenemos por si en el futuro se necesita)
    tipo = Column(String(10), nullable=False, index=True, default="entrada")
    
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
    
    # VALIDACIÓN
    is_valid = Column(Boolean, default=True)  # Si la asistencia es válida
    validation_notes = Column(Text)  # Notas sobre validación
    
    # AUDITORÍA
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # CONSTRAINT
    __table_args__ = (
        CheckConstraint("tipo IN ('entrada', 'salida')", name="chk_tipo"),
    )
    
    # RELACIONES
    cooperativista = relationship("Cooperativista", back_populates="attendances")
    period = relationship("AttendancePeriod", back_populates="attendances")
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
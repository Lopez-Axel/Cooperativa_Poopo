from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime, date, time

# ============ ATTENDANCE PERIOD SCHEMAS ============

class AttendancePeriodBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    mes: int  # 1-12
    anio: int  # 2025, 2026, etc.
    fecha_asistencia: date
    hora_inicio: time
    hora_fin: time
    is_active: bool = True

class AttendancePeriodCreate(AttendancePeriodBase):
    pass

class AttendancePeriodUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    fecha_asistencia: Optional[date] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    is_active: Optional[bool] = None
    is_open: Optional[bool] = None

class AttendancePeriodResponse(AttendancePeriodBase):
    id: int
    is_open: bool
    total_expected: int
    total_marked: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    closed_at: Optional[datetime] = None
    closed_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)


# ============ ATTENDANCE SCHEMAS ============

class AttendanceBase(BaseModel):
    cooperativista_id: int
    period_id: Optional[int] = None
    device_id: str
    tipo: Literal["entrada", "salida"] = "entrada"
    fecha: date
    hora: time
    location_lat: float
    location_lon: float
    distance_meters: Optional[int] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceUpdate(BaseModel):
    tipo: Optional[Literal["entrada", "salida"]] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None
    distance_meters: Optional[int] = None
    photo_url: Optional[str] = None
    notes: Optional[str] = None
    is_valid: Optional[bool] = None
    validation_notes: Optional[str] = None

class AttendanceResponse(AttendanceBase):
    id: int
    timestamp: datetime
    is_valid: bool
    validation_notes: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ ATTENDANCE LOG SCHEMAS ============

class AttendanceLogResponse(BaseModel):
    id: int
    attendance_id: int
    action: str
    changed_by: Optional[int] = None
    old_values: Optional[str] = None
    new_values: Optional[str] = None
    reason: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ STATS SCHEMAS ============

class PeriodStatsResponse(BaseModel):
    """Estadísticas de un período de asistencia"""
    period_id: int
    nombre: str
    fecha_asistencia: date
    total_expected: int
    total_marked: int
    pendientes: int
    porcentaje_asistencia: float
    is_open: bool
    
    model_config = ConfigDict(from_attributes=True)
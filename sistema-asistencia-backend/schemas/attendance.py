from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime, date, time

# ============ ATTENDANCE PERIOD SCHEMAS ============

class AttendancePeriodBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    mes: int
    anio: int
    fecha_asistencia: date
    hora_inicio: time
    hora_fin: time
    is_active: bool = True
    is_open: bool = True

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
    tipo: Literal["entrada", "salida"] = "entrada"
    fecha: date
    hora: time

class AttendanceCreate(BaseModel):
    qr_code: str
    period_id: Optional[int] = None
    tipo: Literal["entrada", "salida"] = "entrada"

class AttendanceUpdate(BaseModel):
    tipo: Optional[Literal["entrada", "salida"]] = None
    fecha: Optional[date] = None
    hora: Optional[time] = None

class AttendanceResponse(AttendanceBase):
    id: int
    registered_by: Optional[int] = None
    timestamp: datetime
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

class ManualAttendanceCreate(BaseModel):
    cooperativista_id: int
    period_id: Optional[int] = None
    tipo: Literal["entrada", "salida"] = "entrada"
    reason: Optional[str] = None

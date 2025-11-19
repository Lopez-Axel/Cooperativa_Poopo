from pydantic import BaseModel, ConfigDict
from typing import Optional, Literal
from datetime import datetime, date, time

class AttendanceBase(BaseModel):
    cooperativista_id: int
    device_id: str
    ubicacion_id: Optional[int] = None
    tipo: Literal["entrada", "salida"]
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

class AttendanceResponse(AttendanceBase):
    id: int
    timestamp: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


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
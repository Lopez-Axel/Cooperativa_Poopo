# schemas/device.py (NUEVOS SCHEMAS)
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class DeviceBase(BaseModel):
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None

class DeviceCreate(DeviceBase):
    cooperativista_id: int
    device_id: str
    api_key: str

class DeviceUpdate(DeviceBase):
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: int
    cooperativista_id: int
    device_id: Optional[str]
    is_active: bool
    is_activated: bool
    is_blocked: bool
    registered_at: datetime
    activated_at: Optional[datetime]
    last_seen: Optional[datetime]
    
    class Config:
        from_attributes = True

class DeviceBatchGenerate(BaseModel):
    cuadrilla: Optional[str] = None
    seccion: Optional[str] = None
    cooperativista_ids: Optional[List[int]] = None
    regenerate: bool = False  # Si True, revoca existentes y genera nuevos

class DeviceActivate(BaseModel):
    api_key: str
    device_id: str
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None

class DeviceBatchResponse(BaseModel):
    total_created: int
    total_skipped: int
    devices: List[dict]
    skipped: List[dict]

class DeviceExportData(BaseModel):
    codigo_unico: str
    nombre_completo: str
    ci: str
    cuadrilla: str
    api_key: str
    estado: str
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    cooperativista_id: int
    device_id: str
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    auth_method: Optional[str] = None
    is_active: bool = True
    is_blocked: bool = False

class DeviceCreate(DeviceBase):
    api_key: str  # Se enviará en texto plano, se hasheará en el backend

class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    auth_method: Optional[str] = None
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None
    block_reason: Optional[str] = None

class DeviceResponse(DeviceBase):
    id: int
    api_key_hash: str
    block_reason: Optional[str] = None
    registered_at: datetime
    registered_by: Optional[int] = None
    last_seen: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    revoked_at: Optional[datetime] = None
    revoked_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
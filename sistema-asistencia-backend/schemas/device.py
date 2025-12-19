from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class DeviceBase(BaseModel):
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None

class DeviceLink(BaseModel):
    device_id: str
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None

class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    device_model: Optional[str] = None
    device_os: Optional[str] = None
    is_active: Optional[bool] = None

class DeviceResponse(DeviceBase):
    id: int
    user_id: int
    device_id: str
    is_active: bool
    registered_at: datetime
    deactivated_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class ConfigBase(BaseModel):
    key: str
    value: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[str] = None

class ConfigCreate(ConfigBase):
    pass

class ConfigUpdate(BaseModel):
    value: Optional[str] = None
    description: Optional[str] = None
    data_type: Optional[str] = None

class ConfigResponse(ConfigBase):
    updated_at: datetime
    updated_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
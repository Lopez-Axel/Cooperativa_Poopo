from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class SeccionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    id_delegado: Optional[int] = None
    is_active: bool = True

class SeccionCreate(SeccionBase):
    pass

class SeccionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    id_delegado: Optional[int] = None
    is_active: Optional[bool] = None

class SeccionResponse(SeccionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

class DelegadoInfo(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    ci: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SeccionWithDelegadoResponse(SeccionResponse):
    delegado: Optional[DelegadoInfo] = None
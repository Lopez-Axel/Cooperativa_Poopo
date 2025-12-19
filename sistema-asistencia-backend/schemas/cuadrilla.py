from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CuadrillaBase(BaseModel):
    nombre: str
    id_seccion: int
    is_active: bool = True

class CuadrillaCreate(CuadrillaBase):
    pass

class CuadrillaUpdate(BaseModel):
    nombre: Optional[str] = None
    id_seccion: Optional[int] = None
    is_active: Optional[bool] = None

class CuadrillaResponse(CuadrillaBase):
    id: int
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)

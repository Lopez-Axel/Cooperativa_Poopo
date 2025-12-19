from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from typing import List

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

class CooperativistaInfo(BaseModel):
    id: int
    nombres: str
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    ci: Optional[str] = None
    rol_cuadrilla: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class SeccionInfo(BaseModel):
    id: int
    nombre: str
    
    model_config = ConfigDict(from_attributes=True)

class CuadrillaDetailsResponse(BaseModel):
    id: int
    nombre: str
    created_at: datetime
    updated_at: datetime
    
    seccion: SeccionInfo
    
    cooperativistas: List[CooperativistaInfo] = []
    total_cooperativistas: int
    
    model_config = ConfigDict(from_attributes=True)
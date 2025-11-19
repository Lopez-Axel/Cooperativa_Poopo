from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class UbicacionBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None
    latitud: float
    longitud: float
    radio_metros: int = 50
    direccion: Optional[str] = None
    is_active: bool = True

class UbicacionCreate(UbicacionBase):
    pass

class UbicacionUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    radio_metros: Optional[int] = None
    direccion: Optional[str] = None
    is_active: Optional[bool] = None

class UbicacionResponse(UbicacionBase):
    id: int
    created_at: datetime
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
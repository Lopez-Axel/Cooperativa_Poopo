from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import date, datetime

class CooperativistaBase(BaseModel):
    nro: int
    seccion: Optional[str] = None
    cuadrilla: Optional[str] = None
    jefe_cuadrilla: Optional[str] = None
    delegado_seccion: Optional[str] = None
    apellido_paterno: str
    apellido_materno: Optional[str] = None
    nombres: str
    ci: Optional[str] = None
    ci_expedido: Optional[str] = None
    ci_foto_url: Optional[str] = None
    documento_abc_url: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_nacimiento: Optional[date] = None
    codigo_asegurado: Optional[str] = None
    cua: Optional[str] = None
    ocupacion: Optional[str] = None
    estado_asegurado: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True

class CooperativistaCreate(CooperativistaBase):
    pass

class CooperativistaUpdate(BaseModel):
    nro: Optional[int] = None
    seccion: Optional[str] = None
    cuadrilla: Optional[str] = None
    jefe_cuadrilla: Optional[str] = None
    delegado_seccion: Optional[str] = None
    apellido_paterno: Optional[str] = None
    apellido_materno: Optional[str] = None
    nombres: Optional[str] = None
    ci: Optional[str] = None
    ci_expedido: Optional[str] = None
    ci_foto_url: Optional[str] = None
    documento_abc_url: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_nacimiento: Optional[date] = None
    codigo_asegurado: Optional[str] = None
    cua: Optional[str] = None
    ocupacion: Optional[str] = None
    estado_asegurado: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    motivo_baja: Optional[str] = None
    fecha_baja: Optional[date] = None

class CooperativistaResponse(CooperativistaBase):
    id: int
    motivo_baja: Optional[str] = None
    fecha_baja: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None
    
    model_config = ConfigDict(from_attributes=True)
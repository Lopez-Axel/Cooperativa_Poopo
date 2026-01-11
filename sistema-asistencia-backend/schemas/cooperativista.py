from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class CooperativistaBase(BaseModel):
    id_cuadrilla: Optional[int] = None
    rol_cuadrilla: Optional[str] = None
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
    usuario_gestora: Optional[str] = None
    password_gestora: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    is_active: bool = True


class CooperativistaCreate(CooperativistaBase):
    pass


class CooperativistaUpdate(BaseModel):
    id_cuadrilla: Optional[int] = None
    rol_cuadrilla: Optional[str] = None
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
    usuario_gestora: Optional[str] = None
    password_gestora: Optional[str] = None
    telefono: Optional[str] = None
    is_active: Optional[bool] = None
    motivo_baja: Optional[str] = None
    fecha_baja: Optional[date] = None


class CooperativistaResponse(CooperativistaBase):
    id: int
    qr_code: str
    motivo_baja: Optional[str] = None
    fecha_baja: Optional[date] = None
    created_at: datetime
    updated_at: datetime
    created_by: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

# routers/devices.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from database import get_db
from models.device import Device
from schemas.device import DeviceCreate, DeviceUpdate, DeviceResponse
from passlib.context import CryptContext

router = APIRouter(prefix="/devices", tags=["devices"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_api_key(api_key: str) -> str:
    return pwd_context.hash(api_key)

def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    return pwd_context.verify(plain_key, hashed_key)

@router.get("/", response_model=List[DeviceResponse])
def get_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cooperativista_id: Optional[int] = None,
    is_active: Optional[bool] = None,
    is_blocked: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Device)
    
    if cooperativista_id:
        query = query.filter(Device.cooperativista_id == cooperativista_id)
    if is_active is not None:
        query = query.filter(Device.is_active == is_active)
    if is_blocked is not None:
        query = query.filter(Device.is_blocked == is_blocked)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

@router.get("/device-id/{device_identifier}", response_model=DeviceResponse)
def get_device_by_identifier(device_identifier: str, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.device_id == device_identifier).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

@router.get("/cooperativista/{cooperativista_id}/devices", response_model=List[DeviceResponse])
def get_cooperativista_devices(cooperativista_id: int, db: Session = Depends(get_db)):
    from models.cooperativista import Cooperativista
    
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == cooperativista_id
    ).first()
    if not cooperativista:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    devices = db.query(Device).filter(
        Device.cooperativista_id == cooperativista_id
    ).all()
    return devices

@router.post("/", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED)
def create_device(device: DeviceCreate, registered_by: Optional[int] = None, db: Session = Depends(get_db)):
    from models.cooperativista import Cooperativista
    
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == device.cooperativista_id
    ).first()
    if not cooperativista:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if not cooperativista.is_active:
        raise HTTPException(status_code=400, detail="Cooperativista inactivo")
    
    existing_device = db.query(Device).filter(Device.device_id == device.device_id).first()
    if existing_device:
        raise HTTPException(status_code=400, detail="El device_id ya está registrado")
    
    active_devices = db.query(Device).filter(
        Device.cooperativista_id == device.cooperativista_id,
        Device.is_active == True
    ).count()
    
    max_devices = 1  # Obtener de config si es necesario
    if active_devices >= max_devices:
        raise HTTPException(
            status_code=400, 
            detail=f"El cooperativista ya tiene el máximo de dispositivos permitidos ({max_devices})"
        )
    
    device_data = device.model_dump(exclude={"api_key"})
    device_data["api_key_hash"] = hash_api_key(device.api_key)
    device_data["registered_by"] = registered_by
    
    db_device = Device(**device_data)
    db.add(db_device)
    db.commit()
    db.refresh(db_device)
    return db_device

@router.put("/{device_id}", response_model=DeviceResponse)
def update_device(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db)
):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    update_data = device.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_device, key, value)
    
    db.commit()
    db.refresh(db_device)
    return db_device

@router.post("/{device_id}/block")
def block_device(
    device_id: int,
    block_reason: str,
    blocked_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db_device.is_blocked = True
    db_device.block_reason = block_reason
    db_device.is_active = False
    
    db.commit()
    return {"message": "Dispositivo bloqueado exitosamente"}

@router.post("/{device_id}/unblock")
def unblock_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db_device.is_blocked = False
    db_device.block_reason = None
    db_device.is_active = True
    
    db.commit()
    return {"message": "Dispositivo desbloqueado exitosamente"}

@router.post("/{device_id}/revoke")
def revoke_device(
    device_id: int,
    revoked_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db_device.is_active = False
    db_device.revoked_at = datetime.now()
    db_device.revoked_by = revoked_by
    
    db.commit()
    return {"message": "Dispositivo revocado exitosamente"}

@router.post("/{device_id}/update-activity")
def update_device_activity(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db_device.last_seen = datetime.now()
    db_device.last_activity = datetime.now()
    
    db.commit()
    return {"message": "Actividad actualizada"}

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db.delete(db_device)
    db.commit()
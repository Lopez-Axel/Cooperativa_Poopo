from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from utils.dependencies import get_db, get_current_user
from services.device_service import device_service
from schemas.device import DeviceLink, DeviceResponse

router = APIRouter(prefix="/devices", tags=["Devices"])

@router.post("/link", response_model=DeviceResponse)
def link_device(
    device_data: DeviceLink,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return device_service.link_device(db, current_user.id, device_data)

@router.get("/me", response_model=List[DeviceResponse])
def get_my_devices(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return device_service.get_user_devices(db, current_user.id)

@router.get("/active", response_model=DeviceResponse)
def get_active_device(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return device_service.get_active_device(db, current_user.id)

@router.post("/{device_id}/deactivate", response_model=DeviceResponse)
def deactivate_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return device_service.deactivate_device(db, current_user.id, device_id)
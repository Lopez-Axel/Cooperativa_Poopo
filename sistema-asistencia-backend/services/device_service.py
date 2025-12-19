from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.device_repo import device_repo
from models.device import Device
from schemas.device import DeviceLink, DeviceResponse

class DeviceService:
    
    def link_device(self, db: Session, user_id: int, device_data: DeviceLink) -> DeviceResponse:
        existing_device = device_repo.get_by_device_id(db, device_data.device_id)
        
        if existing_device and existing_device.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dispositivo ya vinculado a otro usuario"
            )
        
        device_repo.deactivate_all_by_user(db, user_id)
        
        if existing_device and existing_device.user_id == user_id:
            existing_device.is_active = True
            existing_device.deactivated_at = None
            existing_device.device_name = device_data.device_name
            existing_device.device_model = device_data.device_model
            existing_device.device_os = device_data.device_os
            device = device_repo.update(db, existing_device)
        else:
            device = Device(
                user_id=user_id,
                device_id=device_data.device_id,
                device_name=device_data.device_name,
                device_model=device_data.device_model,
                device_os=device_data.device_os,
                is_active=True
            )
            device = device_repo.create(db, device)
        
        return DeviceResponse.model_validate(device)
    
    def get_user_devices(self, db: Session, user_id: int):
        devices = device_repo.get_by_user(db, user_id)
        return [DeviceResponse.model_validate(d) for d in devices]
    
    def get_active_device(self, db: Session, user_id: int):
        device = device_repo.get_active_by_user(db, user_id)
        if not device:
            return None
        return DeviceResponse.model_validate(device)
    
    def deactivate_device(self, db: Session, user_id: int, device_id: int) -> DeviceResponse:
        device = device_repo.get_by_id(db, device_id)
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Dispositivo no encontrado"
            )
        
        if device.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No autorizado"
            )
        
        device.is_active = False
        from sqlalchemy import func
        device.deactivated_at = func.now()
        device = device_repo.update(db, device)
        
        return DeviceResponse.model_validate(device)

device_service = DeviceService()
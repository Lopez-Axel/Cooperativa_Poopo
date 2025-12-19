from sqlalchemy.orm import Session
from sqlalchemy import func
from models.device import Device
from typing import Optional, List

class DeviceRepository:
    
    def get_by_id(self, db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()
    
    def get_by_device_id(self, db: Session, device_id: str) -> Optional[Device]:
        return db.query(Device).filter(Device.device_id == device_id).first()
    
    def get_by_user(self, db: Session, user_id: int) -> List[Device]:
        return db.query(Device).filter(Device.user_id == user_id).all()
    
    def get_active_by_user(self, db: Session, user_id: int) -> Optional[Device]:
        return db.query(Device).filter(
            Device.user_id == user_id,
            Device.is_active == True
        ).first()
    
    def create(self, db: Session, device: Device) -> Device:
        db.add(device)
        db.commit()
        db.refresh(device)
        return device
    
    def update(self, db: Session, device: Device) -> Device:
        db.commit()
        db.refresh(device)
        return device
    
    def deactivate_all_by_user(self, db: Session, user_id: int) -> None:
        db.query(Device).filter(Device.user_id == user_id).update({
            "is_active": False,
            "deactivated_at": func.now()
        })
        db.commit()
    
    def update_last_seen(self, db: Session, device_id: int) -> None:
        db.query(Device).filter(Device.id == device_id).update({"last_seen": func.now()})
        db.commit()
    
    def delete(self, db: Session, device: Device) -> None:
        db.delete(device)
        db.commit()

device_repo = DeviceRepository()
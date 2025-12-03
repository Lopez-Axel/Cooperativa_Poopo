# routers/devices.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import Integer
from sqlalchemy import and_, or_
from typing import List, Optional
from datetime import datetime
import secrets
import string
from database import get_db
from models.device import Device
from models.cooperativista import Cooperativista
from schemas.device import (
    DeviceCreate, DeviceUpdate, DeviceResponse, 
    DeviceBatchGenerate, DeviceActivate, DeviceBatchResponse,
    DeviceExportData
)
from passlib.context import CryptContext

router = APIRouter(prefix="/devices", tags=["devices"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_api_key(api_key: str) -> str:
    return pwd_context.hash(api_key)

def verify_api_key(plain_key: str, hashed_key: str) -> bool:
    return pwd_context.verify(plain_key, hashed_key)

def generate_api_key(length: int = 32) -> str:
    """Genera una API key segura y legible"""
    characters = string.ascii_uppercase + string.digits
    # Evitamos caracteres confusos: 0, O, I, 1
    characters = characters.replace('0', '').replace('O', '').replace('I', '').replace('1', '')
    api_key = ''.join(secrets.choice(characters) for _ in range(length))
    # Formato: XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX-XXXX
    formatted = '-'.join([api_key[i:i+4] for i in range(0, len(api_key), 4)])
    return formatted

@router.get("/", response_model=List[DeviceResponse])
def get_devices(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cooperativista_id: Optional[int] = None,
    cuadrilla: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_activated: Optional[bool] = None,
    is_blocked: Optional[bool] = None,
    include_revoked: bool = Query(False),
    db: Session = Depends(get_db)
):
    query = db.query(Device)
    
    # FILTRO CRÍTICO: No mostrar revocados por defecto
    if not include_revoked:
        query = query.filter(Device.revoked_at == None)
    
    if cooperativista_id:
        query = query.filter(Device.cooperativista_id == cooperativista_id)
    
    if cuadrilla:
        query = query.join(Cooperativista).filter(Cooperativista.cuadrilla == cuadrilla)
    
    if is_active is not None:
        query = query.filter(Device.is_active == is_active)
    
    if is_activated is not None:
        query = query.filter(Device.is_activated == is_activated)
    
    if is_blocked is not None:
        query = query.filter(Device.is_blocked == is_blocked)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{device_id}", response_model=DeviceResponse)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return device

@router.get("/validate/{device_id}")
def validate_device(device_id: str, db: Session = Depends(get_db)):
    """
    Valida si un dispositivo puede seguir operando
    La app debe llamar este endpoint al iniciar y periódicamente
    """
    device = db.query(Device).filter(Device.device_id == device_id).first()
    
    if not device:
        return {
            "valid": False,
            "reason": "not_found",
            "message": "Dispositivo no encontrado",
            "should_logout": True
        }
    
    # Verificar si está revocado
    if device.revoked_at is not None:
        return {
            "valid": False,
            "reason": "revoked",
            "message": "Este dispositivo ha sido revocado. Contacte a la administración.",
            "should_logout": True
        }
    
    # Verificar si está bloqueado
    if device.is_blocked:
        return {
            "valid": False,
            "reason": "blocked",
            "message": f"Dispositivo bloqueado: {device.block_reason}",
            "should_logout": True
        }
    
    # Verificar si está inactivo
    if not device.is_active:
        return {
            "valid": False,
            "reason": "inactive",
            "message": "Dispositivo inactivo",
            "should_logout": True
        }
    
    # Verificar si el cooperativista está activo
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == device.cooperativista_id
    ).first()
    
    if not cooperativista or not cooperativista.is_active:
        return {
            "valid": False,
            "reason": "cooperativista_inactive",
            "message": "Cooperativista inactivo",
            "should_logout": True
        }
    
    # Actualizar last_seen
    device.last_seen = datetime.now()
    db.commit()
    
    return {
        "valid": True,
        "cooperativista_id": device.cooperativista_id,
        "cooperativista_nombre": f"{cooperativista.nombres} {cooperativista.apellido_paterno}"
    }

@router.post("/generate-batch", response_model=DeviceBatchResponse)
def generate_batch_api_keys(
    batch: DeviceBatchGenerate,
    registered_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Genera API keys masivas por cuadrilla, sección o lista de IDs
    """
    query = db.query(Cooperativista).filter(Cooperativista.is_active == True)
    
    if batch.cuadrilla:
        query = query.filter(Cooperativista.cuadrilla == batch.cuadrilla)
    
    if batch.seccion:
        query = query.filter(Cooperativista.seccion == batch.seccion)
    
    if batch.cooperativista_ids:
        query = query.filter(Cooperativista.id.in_(batch.cooperativista_ids))
    
    cooperativistas = query.all()
    
    if not cooperativistas:
        raise HTTPException(
            status_code=404, 
            detail="No se encontraron cooperativistas con los criterios especificados"
        )
    
    created_devices = []
    skipped = []
    
    for coop in cooperativistas:
        # CRÍTICO: Buscar dispositivos NO revocados
        existing_device = db.query(Device).filter(
            Device.cooperativista_id == coop.id,
            Device.revoked_at == None
        ).first()
        
        if existing_device and not batch.regenerate:
            skipped.append({
                "cooperativista_id": coop.id,
                "nombre": f"{coop.nombres} {coop.apellido_paterno}",
                "reason": "Ya tiene dispositivo activo registrado"
            })
            continue
        
        if existing_device and batch.regenerate:
            # Revocar el anterior (liberar device_id)
            existing_device.device_id = None
            existing_device.device_name = None
            existing_device.device_model = None
            existing_device.device_os = None
            existing_device.is_active = False
            existing_device.is_activated = False
            existing_device.revoked_at = datetime.now()
            existing_device.revoked_by = registered_by
        
        # Generar nueva API key
        api_key = generate_api_key()
        
        # Crear dispositivo
        new_device = Device(
            cooperativista_id=coop.id,
            api_key_plain=api_key,
            api_key_hash=hash_api_key(api_key),
            auth_method="api_key",
            is_active=False,
            is_activated=False,
            registered_by=registered_by,
            registered_at=datetime.now()
        )
        
        db.add(new_device)
        created_devices.append({
            "device_id": None,
            "cooperativista_id": coop.id,
            "nombre_completo": f"{coop.nombres} {coop.apellido_paterno} {coop.apellido_materno or ''}".strip(),
            "cuadrilla": coop.cuadrilla,
            "api_key": api_key
        })
    
    db.commit()
    
    # Actualizar IDs después del commit
    for idx, coop in enumerate([c for c in cooperativistas if c.id not in [s["cooperativista_id"] for s in skipped]]):
        device = db.query(Device).filter(
            Device.cooperativista_id == coop.id,
            Device.is_activated == False,
            Device.revoked_at == None
        ).order_by(Device.registered_at.desc()).first()
        
        if device:
            created_devices[idx]["device_id"] = device.id
    
    return {
        "total": len(cooperativistas),
        "created": len(created_devices),
        "skipped": len(skipped),
        "devices": created_devices
    }

@router.post("/activate", response_model=DeviceResponse)
def activate_device(
    activation: DeviceActivate,
    db: Session = Depends(get_db)
):
    """
    Activa un dispositivo vinculándolo con el device_id real del móvil
    """
    # Buscar dispositivo por API key
    device = db.query(Device).filter(
        Device.api_key_plain == activation.api_key
    ).first()
    
    if not device:
        raise HTTPException(status_code=404, detail="API Key inválida")
    
    # CRÍTICO: Verificar si está revocado
    if device.revoked_at is not None:
        raise HTTPException(
            status_code=403, 
            detail="Este código de activación ha sido revocado. Solicite uno nuevo a la administración."
        )
    
    if device.is_blocked:
        raise HTTPException(
            status_code=403, 
            detail="Dispositivo bloqueado. Contacte a la administración."
        )
    
    if device.is_activated:
        raise HTTPException(
            status_code=400, 
            detail="Este dispositivo ya fue activado"
        )
    
    # Verificar que el cooperativista esté activo
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == device.cooperativista_id
    ).first()
    
    if not cooperativista or not cooperativista.is_active:
        raise HTTPException(
            status_code=400, 
            detail="Cooperativista inactivo"
        )
    
    # Verificar que el device_id no esté usado por otro
    existing = db.query(Device).filter(
        Device.device_id == activation.device_id,
        Device.id != device.id,
        Device.revoked_at == None
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=400, 
            detail="Este dispositivo ya está registrado por otro cooperativista"
        )
    
    # Actualizar dispositivo
    device.device_id = activation.device_id
    device.device_name = activation.device_name
    device.device_model = activation.device_model
    device.device_os = activation.device_os
    device.is_active = True
    device.is_activated = True
    device.activated_at = datetime.now()
    device.last_seen = datetime.now()
    device.last_activity = datetime.now()
    
    db.commit()
    db.refresh(device)
    
    return device

@router.get("/export/cuadrilla/{cuadrilla}")
def export_cuadrilla_devices(
    cuadrilla: str,
    db: Session = Depends(get_db)
):
    """
    Exporta dispositivos de una cuadrilla para distribución
    SOLO dispositivos NO revocados y pendientes de activación
    """
    devices = db.query(Device).join(Cooperativista).filter(
        Cooperativista.cuadrilla == cuadrilla,
        Device.is_activated == False,
        Device.revoked_at == None
    ).all()
    
    if not devices:
        raise HTTPException(
            status_code=404, 
            detail="No hay dispositivos pendientes de activación para esta cuadrilla"
        )
    
    export_data = []
    for device in devices:
        coop = device.cooperativista
        export_data.append({
            "id": device.id,
            "nombre_completo": f"{coop.nombres} {coop.apellido_paterno} {coop.apellido_materno or ''}".strip(),
            "ci": coop.ci or "SIN CI",
            "cuadrilla": coop.cuadrilla,
            "api_key": device.api_key_plain,
            "estado": "Pendiente de Activación"
        })
    
    return {
        "cuadrilla": cuadrilla,
        "total": len(export_data),
        "devices": export_data
    }

@router.get("/stats/activation")
def get_activation_stats(db: Session = Depends(get_db)):
    """
    Estadísticas de activación de dispositivos
    SOLO dispositivos NO revocados
    """
    base_query = db.query(Device).filter(Device.revoked_at == None)
    
    total_generated = base_query.count()
    total_activated = base_query.filter(Device.is_activated == True).count()
    total_pending = base_query.filter(Device.is_activated == False).count()
    total_blocked = base_query.filter(Device.is_blocked == True).count()
    
    # Por cuadrilla - SOLO NO revocados
    from sqlalchemy import func as sql_func
    by_cuadrilla = db.query(
        Cooperativista.cuadrilla,
        sql_func.count(Device.id).label("total"),
        sql_func.sum(sql_func.cast(Device.is_activated, Integer)).label("activated"),
        sql_func.sum(sql_func.cast(~Device.is_activated, Integer)).label("pending")
    ).join(Cooperativista).filter(
        Device.revoked_at == None
    ).group_by(Cooperativista.cuadrilla).all()
    
    cuadrilla_stats = [
        {
            "cuadrilla": c.cuadrilla,
            "total": c.total,
            "activated": c.activated or 0,
            "pending": c.pending or 0,
            "percentage": round((c.activated or 0) / c.total * 100, 2) if c.total > 0 else 0
        }
        for c in by_cuadrilla
    ]
    
    return {
        "total_generated": total_generated,
        "total_activated": total_activated,
        "total_pending": total_pending,
        "total_blocked": total_blocked,
        "activation_percentage": round(total_activated / total_generated * 100, 2) if total_generated > 0 else 0,
        "by_cuadrilla": cuadrilla_stats
    }

@router.post("/{device_id}/block")
def block_device(
    device_id: int,
    block_reason: str,
    blocked_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Bloquea un dispositivo TEMPORALMENTE
    - NO libera el device_id (el hardware sigue asociado)
    - Puede ser desbloqueado
    - El API Key sigue siendo válido
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    if db_device.revoked_at is not None:
        raise HTTPException(
            status_code=400, 
            detail="No se puede bloquear un dispositivo revocado"
        )
    
    db_device.is_blocked = True
    db_device.block_reason = block_reason
    db_device.is_active = False
    
    db.commit()
    
    return {
        "message": "Dispositivo bloqueado exitosamente",
        "can_unblock": True
    }

@router.post("/{device_id}/unblock")
def unblock_device(device_id: int, db: Session = Depends(get_db)):
    """
    Desbloquea un dispositivo
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db_device.is_blocked = False
    db_device.block_reason = None
    if db_device.is_activated:
        db_device.is_active = True
    
    db.commit()
    return {"message": "Dispositivo desbloqueado exitosamente"}

@router.post("/{device_id}/deactivate")
def deactivate_device(
    device_id: int,
    db: Session = Depends(get_db)
):
    """
    Desactiva un dispositivo TEMPORALMENTE (libera el API Key para reutilización)
    
    Diferencia con revoke:
    - deactivate: El usuario puede volver con el MISMO API Key
    - revoke: El API Key queda invalidado permanentemente
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    if not db_device.is_activated:
        raise HTTPException(
            status_code=400, 
            detail="El dispositivo no está activado, no se puede desactivar"
        )

    db_device.is_activated = False
    db_device.is_active = False
    db_device.device_id = None
    db_device.device_name = None
    db_device.device_model = None
    db_device.device_os = None
    db_device.activated_at = None
    db_device.last_activity = datetime.now()
    
    db.commit()
    db.refresh(db_device)
    
    return {
        "message": "Dispositivo desactivado exitosamente",
        "device_id": db_device.id,
        "cooperativista_id": db_device.cooperativista_id,
        "can_reactivate": True,
        "api_key_status": "válido para reactivación"
    }

@router.post("/{device_id}/revoke")
def revoke_device(
    device_id: int,
    revoked_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """
    Revoca un dispositivo PERMANENTEMENTE
    - Libera el device_id para que pueda ser usado por otro cooperativista
    - El API Key queda invalidado
    - Se debe generar un nuevo batch para reactivar
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    # CRÍTICO: Liberar device_id para permitir reutilización del hardware
    db_device.device_id = None
    db_device.device_name = None
    db_device.device_model = None
    db_device.device_os = None
    
    # Marcar como revocado
    db_device.is_active = False
    db_device.is_activated = False
    db_device.revoked_at = datetime.now()
    db_device.revoked_by = revoked_by
    
    db.commit()
    
    return {
        "message": "Dispositivo revocado exitosamente",
        "device_id": db_device.id,
        "cooperativista_id": db_device.cooperativista_id,
        "device_hardware_freed": True,
        "requires_new_api_key": True
    }

@router.delete("/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    """
    Elimina físicamente un dispositivo
    USAR CON PRECAUCIÓN
    """
    db_device = db.query(Device).filter(Device.id == device_id).first()
    if not db_device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    
    db.delete(db_device)
    db.commit()
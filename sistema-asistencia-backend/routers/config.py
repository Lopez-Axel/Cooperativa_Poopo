# routers/config.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Union
from database import get_db
from models.config import Config
from schemas.config import ConfigCreate, ConfigUpdate, ConfigResponse

router = APIRouter(prefix="/config", tags=["config"])

def parse_config_value(value: str, data_type: str) -> Any:
    """Convierte el valor string al tipo de dato correcto"""
    if not value:
        return None
    
    if data_type == "integer":
        return int(value)
    elif data_type == "float":
        return float(value)
    elif data_type == "boolean":
        return value.lower() in ("true", "1", "yes")
    else:  # string por defecto
        return value

def validate_data_type(value: str, data_type: str) -> bool:
    """Valida que el valor sea compatible con el tipo de dato"""
    try:
        parse_config_value(value, data_type)
        return True
    except (ValueError, AttributeError):
        return False

@router.get("/", response_model=List[ConfigResponse])
def get_all_config(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    data_type: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Config)
    
    if data_type:
        query = query.filter(Config.data_type == data_type)
    if search:
        query = query.filter(
            (Config.key.ilike(f"%{search}%")) |
            (Config.description.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/{key}", response_model=ConfigResponse)
def get_config(key: str, db: Session = Depends(get_db)):
    config = db.query(Config).filter(Config.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    return config

@router.get("/{key}/value")
def get_config_value(key: str, db: Session = Depends(get_db)) -> dict:
    """Retorna solo el valor parseado según su tipo de dato"""
    config = db.query(Config).filter(Config.key == key).first()
    if not config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    parsed_value = parse_config_value(config.value, config.data_type)
    
    return {
        "key": config.key,
        "value": parsed_value,
        "data_type": config.data_type
    }

@router.get("/type/{data_type}", response_model=List[ConfigResponse])
def get_config_by_type(
    data_type: str,
    db: Session = Depends(get_db)
):
    """Obtiene todas las configuraciones de un tipo específico"""
    configs = db.query(Config).filter(Config.data_type == data_type).all()
    return configs

@router.post("/", response_model=ConfigResponse, status_code=status.HTTP_201_CREATED)
def create_config(
    config: ConfigCreate,
    updated_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    existing = db.query(Config).filter(Config.key == config.key).first()
    if existing:
        raise HTTPException(status_code=400, detail="La clave de configuración ya existe")
    
    if config.data_type and config.value:
        if not validate_data_type(config.value, config.data_type):
            raise HTTPException(
                status_code=400,
                detail=f"El valor no es compatible con el tipo de dato '{config.data_type}'"
            )
    
    config_data = config.model_dump()
    config_data["updated_by"] = updated_by
    
    db_config = Config(**config_data)
    db.add(db_config)
    db.commit()
    db.refresh(db_config)
    return db_config

@router.put("/{key}", response_model=ConfigResponse)
def update_config(
    key: str,
    config: ConfigUpdate,
    updated_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    db_config = db.query(Config).filter(Config.key == key).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    update_data = config.model_dump(exclude_unset=True)
    
    if "value" in update_data and update_data["value"]:
        data_type = update_data.get("data_type", db_config.data_type)
        if not validate_data_type(update_data["value"], data_type):
            raise HTTPException(
                status_code=400,
                detail=f"El valor no es compatible con el tipo de dato '{data_type}'"
            )
    
    for field, value in update_data.items():
        setattr(db_config, field, value)
    
    db_config.updated_by = updated_by
    
    db.commit()
    db.refresh(db_config)
    return db_config

@router.delete("/{key}", status_code=status.HTTP_204_NO_CONTENT)
def delete_config(key: str, db: Session = Depends(get_db)):
    db_config = db.query(Config).filter(Config.key == key).first()
    if not db_config:
        raise HTTPException(status_code=404, detail="Configuración no encontrada")
    
    db.delete(db_config)
    db.commit()

@router.post("/bulk-update")
def bulk_update_config(
    configs: dict[str, str],
    updated_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Actualiza múltiples configuraciones a la vez"""
    updated_keys = []
    errors = []
    
    for key, value in configs.items():
        db_config = db.query(Config).filter(Config.key == key).first()
        
        if not db_config:
            errors.append({"key": key, "error": "Configuración no encontrada"})
            continue
        
        if not validate_data_type(value, db_config.data_type):
            errors.append({
                "key": key,
                "error": f"Valor incompatible con tipo '{db_config.data_type}'"
            })
            continue
        
        db_config.value = value
        db_config.updated_by = updated_by
        updated_keys.append(key)
    
    db.commit()
    
    return {
        "updated": updated_keys,
        "errors": errors,
        "total_updated": len(updated_keys),
        "total_errors": len(errors)
    }

@router.get("/system/info")
def get_system_info(db: Session = Depends(get_db)):
    """Retorna información del sistema basada en configuraciones"""
    configs = db.query(Config).all()
    
    system_info = {}
    for config in configs:
        system_info[config.key] = {
            "value": parse_config_value(config.value, config.data_type),
            "description": config.description,
            "type": config.data_type
        }
    
    return system_info
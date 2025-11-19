# routers/ubicaciones.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.ubicacion import Ubicacion
from schemas.ubicacion import UbicacionCreate, UbicacionUpdate, UbicacionResponse
from math import radians, cos, sin, asin, sqrt

router = APIRouter(prefix="/ubicaciones", tags=["ubicaciones"])

def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia entre dos puntos GPS usando la fórmula de Haversine.
    Retorna la distancia en metros.
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radio de la Tierra en metros
    
    return c * r

@router.get("/", response_model=List[UbicacionResponse])
def get_ubicaciones(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Ubicacion)
    
    if is_active is not None:
        query = query.filter(Ubicacion.is_active == is_active)
    if search:
        query = query.filter(
            (Ubicacion.nombre.ilike(f"%{search}%")) |
            (Ubicacion.descripcion.ilike(f"%{search}%")) |
            (Ubicacion.direccion.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()

@router.get("/{ubicacion_id}", response_model=UbicacionResponse)
def get_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return ubicacion

@router.get("/validate/gps")
def validate_gps_location(
    lat: float = Query(..., description="Latitud actual"),
    lon: float = Query(..., description="Longitud actual"),
    db: Session = Depends(get_db)
):
    """
    Valida si las coordenadas GPS están dentro del radio permitido de alguna ubicación activa.
    Retorna la ubicación más cercana si está dentro del radio, o error si no.
    """
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.is_active == True).all()
    
    if not ubicaciones:
        raise HTTPException(
            status_code=404, 
            detail="No hay ubicaciones activas registradas"
        )
    
    ubicaciones_validas = []
    
    for ubicacion in ubicaciones:
        distancia = calcular_distancia(lat, lon, ubicacion.latitud, ubicacion.longitud)
        
        if distancia <= ubicacion.radio_metros:
            ubicaciones_validas.append({
                "ubicacion_id": ubicacion.id,
                "nombre": ubicacion.nombre,
                "distancia_metros": round(distancia, 2),
                "radio_permitido": ubicacion.radio_metros,
                "dentro_rango": True
            })
    
    if ubicaciones_validas:
        ubicacion_mas_cercana = min(ubicaciones_validas, key=lambda x: x["distancia_metros"])
        return {
            "valido": True,
            "ubicacion": ubicacion_mas_cercana,
            "todas_ubicaciones_validas": ubicaciones_validas
        }
    
    ubicacion_mas_cercana = min(
        ubicaciones,
        key=lambda u: calcular_distancia(lat, lon, u.latitud, u.longitud)
    )
    distancia_mas_cercana = calcular_distancia(
        lat, lon, ubicacion_mas_cercana.latitud, ubicacion_mas_cercana.longitud
    )
    
    return {
        "valido": False,
        "mensaje": "Fuera del radio permitido",
        "ubicacion_mas_cercana": {
            "ubicacion_id": ubicacion_mas_cercana.id,
            "nombre": ubicacion_mas_cercana.nombre,
            "distancia_metros": round(distancia_mas_cercana, 2),
            "radio_permitido": ubicacion_mas_cercana.radio_metros,
            "diferencia": round(distancia_mas_cercana - ubicacion_mas_cercana.radio_metros, 2)
        }
    }

@router.get("/nearest/location")
def get_nearest_location(
    lat: float = Query(..., description="Latitud actual"),
    lon: float = Query(..., description="Longitud actual"),
    db: Session = Depends(get_db)
):
    """
    Retorna la ubicación más cercana independientemente del radio.
    """
    ubicaciones = db.query(Ubicacion).filter(Ubicacion.is_active == True).all()
    
    if not ubicaciones:
        raise HTTPException(
            status_code=404, 
            detail="No hay ubicaciones activas registradas"
        )
    
    ubicaciones_con_distancia = []
    for ubicacion in ubicaciones:
        distancia = calcular_distancia(lat, lon, ubicacion.latitud, ubicacion.longitud)
        ubicaciones_con_distancia.append({
            "ubicacion_id": ubicacion.id,
            "nombre": ubicacion.nombre,
            "descripcion": ubicacion.descripcion,
            "latitud": ubicacion.latitud,
            "longitud": ubicacion.longitud,
            "radio_metros": ubicacion.radio_metros,
            "distancia_metros": round(distancia, 2),
            "dentro_rango": distancia <= ubicacion.radio_metros
        })
    
    ubicaciones_con_distancia.sort(key=lambda x: x["distancia_metros"])
    
    return {
        "ubicacion_mas_cercana": ubicaciones_con_distancia[0],
        "todas_ubicaciones": ubicaciones_con_distancia
    }

@router.post("/", response_model=UbicacionResponse, status_code=status.HTTP_201_CREATED)
def create_ubicacion(
    ubicacion: UbicacionCreate,
    created_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    ubicacion_data = ubicacion.model_dump()
    ubicacion_data["created_by"] = created_by
    
    db_ubicacion = Ubicacion(**ubicacion_data)
    db.add(db_ubicacion)
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@router.put("/{ubicacion_id}", response_model=UbicacionResponse)
def update_ubicacion(
    ubicacion_id: int,
    ubicacion: UbicacionUpdate,
    db: Session = Depends(get_db)
):
    db_ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    update_data = ubicacion.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_ubicacion, key, value)
    
    db.commit()
    db.refresh(db_ubicacion)
    return db_ubicacion

@router.delete("/{ubicacion_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    db_ubicacion = db.query(Ubicacion).filter(Ubicacion.id == ubicacion_id).first()
    if not db_ubicacion:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    
    db.delete(db_ubicacion)
    db.commit()
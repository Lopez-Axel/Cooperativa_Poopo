from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, extract
from typing import List, Optional
from datetime import date, datetime, time
from database import get_db
from models.attendance import AttendancePeriod, Attendance
from models.cooperativista import Cooperativista
from schemas.attendance import (
    AttendancePeriodCreate,
    AttendancePeriodUpdate,
    AttendancePeriodResponse,
    PeriodStatsResponse
)
import json

router = APIRouter(prefix="/attendance-periods", tags=["attendance-periods"])


@router.get("/", response_model=List[AttendancePeriodResponse])
def get_periods(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    mes: Optional[int] = None,
    anio: Optional[int] = None,
    is_active: Optional[bool] = None,
    is_open: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de períodos de asistencia con filtros opcionales"""
    query = db.query(AttendancePeriod)
    
    if mes is not None:
        query = query.filter(AttendancePeriod.mes == mes)
    if anio is not None:
        query = query.filter(AttendancePeriod.anio == anio)
    if is_active is not None:
        query = query.filter(AttendancePeriod.is_active == is_active)
    if is_open is not None:
        query = query.filter(AttendancePeriod.is_open == is_open)
    
    query = query.order_by(AttendancePeriod.anio.desc(), AttendancePeriod.mes.desc(), AttendancePeriod.fecha_asistencia.desc())
    return query.offset(skip).limit(limit).all()


@router.get("/current", response_model=List[AttendancePeriodResponse])
def get_current_periods(db: Session = Depends(get_db)):
    """Obtener períodos del mes actual"""
    today = date.today()
    periods = db.query(AttendancePeriod).filter(
        and_(
            AttendancePeriod.mes == today.month,
            AttendancePeriod.anio == today.year,
            AttendancePeriod.is_active == True
        )
    ).order_by(AttendancePeriod.fecha_asistencia).all()
    return periods


@router.get("/open", response_model=List[AttendancePeriodResponse])
def get_open_periods(db: Session = Depends(get_db)):
    """Obtener períodos actualmente abiertos para marcar asistencia"""
    periods = db.query(AttendancePeriod).filter(
        and_(
            AttendancePeriod.is_active == True,
            AttendancePeriod.is_open == True
        )
    ).order_by(AttendancePeriod.fecha_asistencia).all()
    return periods


@router.get("/{period_id}", response_model=AttendancePeriodResponse)
def get_period(period_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un período específico"""
    period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    return period


@router.get("/{period_id}/stats", response_model=PeriodStatsResponse)
def get_period_stats(period_id: int, db: Session = Depends(get_db)):
    """Obtener estadísticas de asistencia de un período"""
    period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    
    # Contar cooperativistas activos (esperados)
    total_expected = db.query(func.count(Cooperativista.id)).filter(
        Cooperativista.is_active == True
    ).scalar() or 0
    
    # Contar asistencias marcadas para este período
    total_marked = db.query(func.count(Attendance.id)).filter(
        and_(
            Attendance.period_id == period_id,
            Attendance.is_valid == True
        )
    ).scalar() or 0
    
    pendientes = total_expected - total_marked
    porcentaje = (total_marked / total_expected * 100) if total_expected > 0 else 0
    
    return PeriodStatsResponse(
        period_id=period.id,
        nombre=period.nombre,
        fecha_asistencia=period.fecha_asistencia,
        total_expected=total_expected,
        total_marked=total_marked,
        pendientes=pendientes,
        porcentaje_asistencia=round(porcentaje, 2),
        is_open=period.is_open
    )


@router.post("/", response_model=AttendancePeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(
    period: AttendancePeriodCreate,
    created_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Crear un nuevo período de asistencia"""
    
    # Validar que el mes y año sean válidos
    if period.mes < 1 or period.mes > 12:
        raise HTTPException(status_code=400, detail="Mes inválido (debe ser entre 1-12)")
    
    if period.anio < 2024:
        raise HTTPException(status_code=400, detail="Año inválido")
    
    # Verificar que la fecha de asistencia corresponda al mes/año especificado
    if period.fecha_asistencia.month != period.mes or period.fecha_asistencia.year != period.anio:
        raise HTTPException(
            status_code=400, 
            detail="La fecha de asistencia no corresponde al mes/año especificado"
        )
    
    periodos_existentes = db.query(func.count(AttendancePeriod.id)).filter(
        and_(
            AttendancePeriod.mes == period.mes,
            AttendancePeriod.anio == period.anio,
            AttendancePeriod.is_active == True
        )
    ).scalar()
    
    # Validar que hora_fin sea posterior a hora_inicio
    if period.hora_fin <= period.hora_inicio:
        raise HTTPException(
            status_code=400,
            detail="La hora de fin debe ser posterior a la hora de inicio"
        )
    
    # Crear el período
    db_period = AttendancePeriod(
        **period.model_dump(),
        created_by=created_by,
        is_open=False,  # Por defecto cerrado hasta que el admin lo abra
        total_expected=0,
        total_marked=0
    )
    
    db.add(db_period)
    db.commit()
    db.refresh(db_period)
    return db_period


@router.put("/{period_id}", response_model=AttendancePeriodResponse)
def update_period(
    period_id: int,
    period: AttendancePeriodUpdate,
    db: Session = Depends(get_db)
):
    """Actualizar un período de asistencia"""
    db_period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not db_period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    
    update_data = period.model_dump(exclude_unset=True)
    
    # Validar hora_fin > hora_inicio si se están actualizando
    if "hora_inicio" in update_data or "hora_fin" in update_data:
        hora_inicio = update_data.get("hora_inicio", db_period.hora_inicio)
        hora_fin = update_data.get("hora_fin", db_period.hora_fin)
        if hora_fin <= hora_inicio:
            raise HTTPException(
                status_code=400,
                detail="La hora de fin debe ser posterior a la hora de inicio"
            )
    
    for key, value in update_data.items():
        setattr(db_period, key, value)
    
    db.commit()
    db.refresh(db_period)
    return db_period


@router.post("/{period_id}/open", response_model=AttendancePeriodResponse)
def open_period(
    period_id: int,
    db: Session = Depends(get_db)
):
    """Abrir un período para que los cooperativistas puedan marcar asistencia"""
    period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    
    if not period.is_active:
        raise HTTPException(status_code=400, detail="No se puede abrir un período inactivo")
    
    if period.is_open:
        raise HTTPException(status_code=400, detail="El período ya está abierto")
    
    # Actualizar total esperado al momento de abrir
    total_expected = db.query(func.count(Cooperativista.id)).filter(
        Cooperativista.is_active == True
    ).scalar() or 0
    
    period.is_open = True
    period.total_expected = total_expected
    
    db.commit()
    db.refresh(period)
    return period


@router.post("/{period_id}/close", response_model=AttendancePeriodResponse)
def close_period(
    period_id: int,
    closed_by: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Cerrar un período de asistencia"""
    period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    
    if not period.is_open:
        raise HTTPException(status_code=400, detail="El período ya está cerrado")
    
    # Actualizar total marcado al momento de cerrar
    total_marked = db.query(func.count(Attendance.id)).filter(
        and_(
            Attendance.period_id == period_id,
            Attendance.is_valid == True
        )
    ).scalar() or 0
    
    period.is_open = False
    period.total_marked = total_marked
    period.closed_at = datetime.utcnow()
    period.closed_by = closed_by
    
    db.commit()
    db.refresh(period)
    return period


@router.delete("/{period_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_period(
    period_id: int,
    db: Session = Depends(get_db)
):
    """
    Eliminar un período de asistencia.
    NOTA: Las asistencias asociadas tendrán period_id en NULL (SET NULL).
    """
    period = db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    if not period:
        raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
    
    # Verificar si tiene asistencias asociadas
    has_attendances = db.query(Attendance).filter(Attendance.period_id == period_id).first()
    if has_attendances:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar un período con asistencias registradas. Considere desactivarlo en su lugar."
        )
    
    db.delete(period)
    db.commit()
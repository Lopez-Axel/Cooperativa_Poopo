from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import date, datetime, time as time_type
from database import get_db
from models.attendance import Attendance, AttendanceLog, AttendancePeriod
from models.cooperativista import Cooperativista
from schemas.attendance import (
    AttendanceCreate, 
    AttendanceUpdate, 
    AttendanceResponse,
    AttendanceLogResponse
)
import json

router = APIRouter(prefix="/attendance", tags=["attendance"])


@router.get("/", response_model=List[AttendanceResponse])
def get_attendances(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    cooperativista_id: Optional[int] = None,
    period_id: Optional[int] = None,
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    tipo: Optional[str] = None,
    device_id: Optional[str] = None,
    is_valid: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Obtener registros de asistencia con filtros opcionales"""
    query = db.query(Attendance)
    
    if cooperativista_id:
        query = query.filter(Attendance.cooperativista_id == cooperativista_id)
    if period_id:
        query = query.filter(Attendance.period_id == period_id)
    if fecha_inicio:
        query = query.filter(Attendance.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Attendance.fecha <= fecha_fin)
    if tipo:
        query = query.filter(Attendance.tipo == tipo)
    if device_id:
        query = query.filter(Attendance.device_id == device_id)
    if is_valid is not None:
        query = query.filter(Attendance.is_valid == is_valid)
    
    query = query.order_by(Attendance.timestamp.desc())
    return query.offset(skip).limit(limit).all()


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    """Obtener detalles de un registro de asistencia"""
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    return attendance


@router.get("/cooperativista/{cooperativista_id}/period/{period_id}", response_model=Optional[AttendanceResponse])
def get_cooperativista_period_attendance(
    cooperativista_id: int, 
    period_id: int,
    db: Session = Depends(get_db)
):
    """Verificar si un cooperativista ya marcó asistencia en un período específico"""
    attendance = db.query(Attendance).filter(
        and_(
            Attendance.cooperativista_id == cooperativista_id,
            Attendance.period_id == period_id,
            Attendance.is_valid == True
        )
    ).first()
    return attendance


@router.get("/cooperativista/{cooperativista_id}/today", response_model=List[AttendanceResponse])
def get_today_attendance(cooperativista_id: int, db: Session = Depends(get_db)):
    """Obtener asistencias de hoy para un cooperativista"""
    today = date.today()
    attendances = db.query(Attendance).filter(
        and_(
            Attendance.cooperativista_id == cooperativista_id,
            Attendance.fecha == today
        )
    ).order_by(Attendance.timestamp.asc()).all()
    return attendances


@router.get("/cooperativista/{cooperativista_id}/range", response_model=List[AttendanceResponse])
def get_attendance_range(
    cooperativista_id: int,
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    """Obtener asistencias de un cooperativista en un rango de fechas"""
    attendances = db.query(Attendance).filter(
        and_(
            Attendance.cooperativista_id == cooperativista_id,
            Attendance.fecha >= fecha_inicio,
            Attendance.fecha <= fecha_fin
        )
    ).order_by(Attendance.fecha.desc(), Attendance.timestamp.desc()).all()
    return attendances


@router.post("/", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def create_attendance(attendance: AttendanceCreate, db: Session = Depends(get_db)):
    """Registrar una nueva asistencia"""
    
    # Verificar que el cooperativista existe y está activo
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == attendance.cooperativista_id
    ).first()
    if not cooperativista:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    if not cooperativista.is_active:
        raise HTTPException(status_code=400, detail="Cooperativista inactivo")
    
    # Si se especifica un período, validar que existe y está abierto
    if attendance.period_id:
        period = db.query(AttendancePeriod).filter(
            AttendancePeriod.id == attendance.period_id
        ).first()
        
        if not period:
            raise HTTPException(status_code=404, detail="Período de asistencia no encontrado")
        
        if not period.is_active:
            raise HTTPException(status_code=400, detail="El período de asistencia no está activo")
        
        if not period.is_open:
            raise HTTPException(status_code=400, detail="El período de asistencia está cerrado")
        
        # Validar que la fecha de asistencia corresponda al período
        if attendance.fecha != period.fecha_asistencia:
            raise HTTPException(
                status_code=400,
                detail=f"La fecha debe ser {period.fecha_asistencia.strftime('%Y-%m-%d')}"
            )
        
        # Validar que la hora esté dentro del rango permitido
        if not (period.hora_inicio <= attendance.hora <= period.hora_fin):
            raise HTTPException(
                status_code=400,
                detail=f"La hora debe estar entre {period.hora_inicio.strftime('%H:%M')} y {period.hora_fin.strftime('%H:%M')}"
            )
        
        # Verificar que no haya marcado ya para este período
        existing = db.query(Attendance).filter(
            and_(
                Attendance.cooperativista_id == attendance.cooperativista_id,
                Attendance.period_id == attendance.period_id,
                Attendance.is_valid == True
            )
        ).first()
        
        if existing:
            raise HTTPException(
                status_code=400,
                detail=f"Ya existe un registro de asistencia válido para este período"
            )
    
    # Crear el registro de asistencia
    db_attendance = Attendance(**attendance.model_dump(), is_valid=True)
    db.add(db_attendance)
    
    try:
        db.flush()  # Asignar ID sin commitear
        
        # Crear log de auditoría
        log = AttendanceLog(
            attendance_id=db_attendance.id,
            action="created",
            new_values=json.dumps(attendance.model_dump(), default=str)
        )
        db.add(log)
        
        # Si hay período, actualizar el contador
        if attendance.period_id:
            period = db.query(AttendancePeriod).filter(
                AttendancePeriod.id == attendance.period_id
            ).first()
            if period:
                period.total_marked = db.query(func.count(Attendance.id)).filter(
                    and_(
                        Attendance.period_id == attendance.period_id,
                        Attendance.is_valid == True
                    )
                ).scalar() or 0
        
        db.commit()
        db.refresh(db_attendance)
        return db_attendance
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error al crear asistencia: {str(e)}")


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    changed_by: Optional[int] = None,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Actualizar un registro de asistencia"""
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    # Guardar valores anteriores para el log
    old_values = {
        "tipo": db_attendance.tipo,
        "fecha": str(db_attendance.fecha),
        "hora": str(db_attendance.hora),
        "location_lat": db_attendance.location_lat,
        "location_lon": db_attendance.location_lon,
        "is_valid": db_attendance.is_valid,
        "notes": db_attendance.notes
    }
    
    # Aplicar actualizaciones
    update_data = attendance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attendance, key, value)
    
    # Crear log de auditoría
    log = AttendanceLog(
        attendance_id=attendance_id,
        action="updated",
        changed_by=changed_by,
        old_values=json.dumps(old_values),
        new_values=json.dumps(update_data, default=str),
        reason=reason
    )
    db.add(log)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: int,
    changed_by: Optional[int] = None,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Eliminar un registro de asistencia"""
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    # Guardar valores para el log
    old_values = {
        "cooperativista_id": db_attendance.cooperativista_id,
        "period_id": db_attendance.period_id,
        "tipo": db_attendance.tipo,
        "fecha": str(db_attendance.fecha),
        "hora": str(db_attendance.hora)
    }
    
    # Crear log antes de eliminar
    log = AttendanceLog(
        attendance_id=attendance_id,
        action="deleted",
        changed_by=changed_by,
        old_values=json.dumps(old_values),
        reason=reason
    )
    db.add(log)
    db.commit()
    
    # Actualizar contador del período si existe
    if db_attendance.period_id:
        period = db.query(AttendancePeriod).filter(
            AttendancePeriod.id == db_attendance.period_id
        ).first()
        if period:
            period.total_marked = db.query(func.count(Attendance.id)).filter(
                and_(
                    Attendance.period_id == db_attendance.period_id,
                    Attendance.is_valid == True,
                    Attendance.id != attendance_id  # Excluir el que se va a eliminar
                )
            ).scalar() or 0
    
    # Eliminar la asistencia
    db.delete(db_attendance)
    db.commit()


@router.get("/{attendance_id}/logs", response_model=List[AttendanceLogResponse])
def get_attendance_logs(attendance_id: int, db: Session = Depends(get_db)):
    """Obtener logs de auditoría de un registro de asistencia"""
    logs = db.query(AttendanceLog).filter(
        AttendanceLog.attendance_id == attendance_id
    ).order_by(AttendanceLog.created_at.desc()).all()
    return logs
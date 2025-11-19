# routers/attendance.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional
from datetime import date, datetime
from database import get_db
from models.attendance import Attendance, AttendanceLog
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
    fecha_inicio: Optional[date] = None,
    fecha_fin: Optional[date] = None,
    tipo: Optional[str] = None,
    device_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Attendance)
    
    if cooperativista_id:
        query = query.filter(Attendance.cooperativista_id == cooperativista_id)
    if fecha_inicio:
        query = query.filter(Attendance.fecha >= fecha_inicio)
    if fecha_fin:
        query = query.filter(Attendance.fecha <= fecha_fin)
    if tipo:
        query = query.filter(Attendance.tipo == tipo)
    if device_id:
        query = query.filter(Attendance.device_id == device_id)
    
    query = query.order_by(Attendance.timestamp.desc())
    return query.offset(skip).limit(limit).all()

@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance(attendance_id: int, db: Session = Depends(get_db)):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    return attendance

@router.get("/cooperativista/{cooperativista_id}/today", response_model=List[AttendanceResponse])
def get_today_attendance(cooperativista_id: int, db: Session = Depends(get_db)):
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
    from models.cooperativista import Cooperativista
    
    cooperativista = db.query(Cooperativista).filter(
        Cooperativista.id == attendance.cooperativista_id
    ).first()
    if not cooperativista:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if not cooperativista.is_active:
        raise HTTPException(status_code=400, detail="Cooperativista inactivo")
    
    last_record = db.query(Attendance).filter(
        and_(
            Attendance.cooperativista_id == attendance.cooperativista_id,
            Attendance.fecha == attendance.fecha
        )
    ).order_by(Attendance.timestamp.desc()).first()
    
    if last_record and last_record.tipo == attendance.tipo:
        raise HTTPException(
            status_code=400, 
            detail=f"Ya existe un registro de {attendance.tipo} para hoy"
        )
    
    db_attendance = Attendance(**attendance.model_dump())
    db.add(db_attendance)
    
    log = AttendanceLog(
        attendance_id=db_attendance.id,
        action="created",
        new_values=json.dumps(attendance.model_dump(), default=str)
    )
    db.add(log)
    
    db.commit()
    db.refresh(db_attendance)
    return db_attendance

@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance: AttendanceUpdate,
    changed_by: Optional[int] = None,
    reason: Optional[str] = None,
    db: Session = Depends(get_db)
):
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    old_values = {
        "tipo": db_attendance.tipo,
        "fecha": str(db_attendance.fecha),
        "hora": str(db_attendance.hora),
        "location_lat": db_attendance.location_lat,
        "location_lon": db_attendance.location_lon,
        "notes": db_attendance.notes
    }
    
    update_data = attendance.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_attendance, key, value)
    
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
    db_attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not db_attendance:
        raise HTTPException(status_code=404, detail="Registro de asistencia no encontrado")
    
    old_values = {
        "cooperativista_id": db_attendance.cooperativista_id,
        "tipo": db_attendance.tipo,
        "fecha": str(db_attendance.fecha),
        "hora": str(db_attendance.hora)
    }
    
    log = AttendanceLog(
        attendance_id=attendance_id,
        action="deleted",
        changed_by=changed_by,
        old_values=json.dumps(old_values),
        reason=reason
    )
    db.add(log)
    db.commit()
    
    db.delete(db_attendance)
    db.commit()

@router.get("/{attendance_id}/logs", response_model=List[AttendanceLogResponse])
def get_attendance_logs(attendance_id: int, db: Session = Depends(get_db)):
    logs = db.query(AttendanceLog).filter(
        AttendanceLog.attendance_id == attendance_id
    ).order_by(AttendanceLog.created_at.desc()).all()
    return logs
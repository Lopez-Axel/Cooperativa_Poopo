from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from utils.dependencies import get_db, get_current_user
from services.attendance_service import attendance_service
from schemas.attendance import AttendanceCreate, AttendanceResponse

router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post("/scan", response_model=AttendanceResponse)
def register_attendance(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return attendance_service.register_attendance(db, attendance_data, current_user.id)

@router.get("/cooperativista/{cooperativista_id}", response_model=List[AttendanceResponse])
def get_cooperativista_attendance(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return attendance_service.get_by_cooperativista(db, cooperativista_id)

@router.get("/period/{period_id}", response_model=List[AttendanceResponse])
def get_period_attendance(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return attendance_service.get_by_period(db, period_id)

@router.get("/date/{fecha}", response_model=List[AttendanceResponse])
def get_date_attendance(
    fecha: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return attendance_service.get_by_date(db, fecha)
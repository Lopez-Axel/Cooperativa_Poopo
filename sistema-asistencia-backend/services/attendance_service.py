from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.attendance_repo import attendance_repo, attendance_period_repo
from repositories.cooperativista_repo import cooperativista_repo
from models.attendance import Attendance
from schemas.attendance import AttendanceCreate, AttendanceResponse
from datetime import datetime, date, time

class AttendanceService:
    
    def register_attendance(
        self, 
        db: Session, 
        attendance_data: AttendanceCreate, 
        user_id: int
    ) -> AttendanceResponse:
        cooperativista = cooperativista_repo.get_by_qr_code(db, attendance_data.qr_code)
        
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="QR no válido"
            )
        
        if not cooperativista.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cooperativista inactivo"
            )
        
        period = None
        if attendance_data.period_id:
            period = attendance_period_repo.get_by_id(db, attendance_data.period_id)
            if not period:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Período no encontrado"
                )
            
            if not period.is_open:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Período cerrado"
                )
            
            existing = attendance_repo.get_by_cooperativista_and_period(
                db, cooperativista.id, period.id
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe registro de asistencia para este período"
                )
        
        now = datetime.now()
        
        attendance = Attendance(
            cooperativista_id=cooperativista.id,
            period_id=attendance_data.period_id,
            registered_by=user_id,
            tipo=attendance_data.tipo,
            fecha=now.date(),
            hora=now.time(),
            timestamp=now
        )
        
        attendance = attendance_repo.create(db, attendance)
        
        if period:
            period.total_marked = attendance_repo.count_by_period(db, period.id)
            attendance_period_repo.update(db, period)
        
        return AttendanceResponse.model_validate(attendance)
    
    def get_by_cooperativista(self, db: Session, cooperativista_id: int):
        attendances = attendance_repo.get_by_cooperativista(db, cooperativista_id)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_by_period(self, db: Session, period_id: int):
        attendances = attendance_repo.get_by_period(db, period_id)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_by_date(self, db: Session, fecha: date):
        attendances = attendance_repo.get_by_date(db, fecha)
        return [AttendanceResponse.model_validate(a) for a in attendances]

attendance_service = AttendanceService()
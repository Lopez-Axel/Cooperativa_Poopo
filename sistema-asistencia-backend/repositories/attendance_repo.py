from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.attendance import Attendance, AttendancePeriod, AttendanceLog
from typing import Optional, List
from datetime import date

class AttendancePeriodRepository:
    
    def get_by_id(self, db: Session, period_id: int) -> Optional[AttendancePeriod]:
        return db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    
    def get_active(self, db: Session) -> List[AttendancePeriod]:
        return db.query(AttendancePeriod).filter(AttendancePeriod.is_active == True).all()
    
    def get_open(self, db: Session) -> List[AttendancePeriod]:
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.is_active == True,
            AttendancePeriod.is_open == True
        ).all()
    
    def get_by_date(self, db: Session, fecha: date) -> Optional[AttendancePeriod]:
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.fecha_asistencia == fecha,
            AttendancePeriod.is_active == True
        ).first()
    
    def get_by_month(self, db: Session, mes: int, anio: int) -> List[AttendancePeriod]:
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.mes == mes,
            AttendancePeriod.anio == anio
        ).all()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[AttendancePeriod]:
        return db.query(AttendancePeriod).offset(skip).limit(limit).all()
    
    def create(self, db: Session, period: AttendancePeriod) -> AttendancePeriod:
        db.add(period)
        db.commit()
        db.refresh(period)
        return period
    
    def update(self, db: Session, period: AttendancePeriod) -> AttendancePeriod:
        db.commit()
        db.refresh(period)
        return period
    
    def delete(self, db: Session, period: AttendancePeriod) -> None:
        db.delete(period)
        db.commit()


class AttendanceRepository:
    
    def get_by_id(self, db: Session, attendance_id: int) -> Optional[Attendance]:
        return db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    def get_by_cooperativista(self, db: Session, cooperativista_id: int) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.cooperativista_id == cooperativista_id).all()
    
    def get_by_period(self, db: Session, period_id: int) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.period_id == period_id).all()
    
    def get_by_cooperativista_and_period(self, db: Session, cooperativista_id: int, period_id: int) -> Optional[Attendance]:
        return db.query(Attendance).filter(
            Attendance.cooperativista_id == cooperativista_id,
            Attendance.period_id == period_id
        ).first()
    
    def get_by_date(self, db: Session, fecha: date) -> List[Attendance]:
        return db.query(Attendance).filter(Attendance.fecha == fecha).all()
    
    def get_by_date_range(self, db: Session, start_date: date, end_date: date) -> List[Attendance]:
        return db.query(Attendance).filter(
            and_(Attendance.fecha >= start_date, Attendance.fecha <= end_date)
        ).all()
    
    def count_by_period(self, db: Session, period_id: int) -> int:
        return db.query(Attendance).filter(Attendance.period_id == period_id).count()
    
    def create(self, db: Session, attendance: Attendance) -> Attendance:
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    def update(self, db: Session, attendance: Attendance) -> Attendance:
        db.commit()
        db.refresh(attendance)
        return attendance
    
    def delete(self, db: Session, attendance: Attendance) -> None:
        db.delete(attendance)
        db.commit()


class AttendanceLogRepository:
    
    def get_by_attendance(self, db: Session, attendance_id: int) -> List[AttendanceLog]:
        return db.query(AttendanceLog).filter(AttendanceLog.attendance_id == attendance_id).all()
    
    def create(self, db: Session, log: AttendanceLog) -> AttendanceLog:
        db.add(log)
        db.commit()
        db.refresh(log)
        return log

attendance_period_repo = AttendancePeriodRepository()
attendance_repo = AttendanceRepository()
attendance_log_repo = AttendanceLogRepository()
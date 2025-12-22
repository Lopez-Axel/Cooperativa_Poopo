from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from models.attendance import Attendance, AttendancePeriod, AttendanceLog
from typing import Optional, List
from datetime import date


class AttendancePeriodRepository:
    """
    Repositorio para gestionar períodos de asistencia.
    """
    
    def get_by_id(self, db: Session, period_id: int) -> Optional[AttendancePeriod]:
        """Obtener un período por su ID."""
        return db.query(AttendancePeriod).filter(AttendancePeriod.id == period_id).first()
    
    def get_active(self, db: Session) -> List[AttendancePeriod]:
        """Obtener todos los períodos activos."""
        return db.query(AttendancePeriod).filter(AttendancePeriod.is_active == True).all()
    
    def get_open(self, db: Session) -> List[AttendancePeriod]:
        """Obtener todos los períodos activos y abiertos."""
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.is_active == True,
            AttendancePeriod.is_open == True
        ).all()
    
    def get_by_date(self, db: Session, fecha: date) -> Optional[AttendancePeriod]:
        """Obtener el período activo para una fecha específica."""
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.fecha_asistencia == fecha,
            AttendancePeriod.is_active == True
        ).first()
    
    def get_by_month(self, db: Session, mes: int, anio: int) -> List[AttendancePeriod]:
        """Obtener todos los períodos de un mes y año específicos."""
        return db.query(AttendancePeriod).filter(
            AttendancePeriod.mes == mes,
            AttendancePeriod.anio == anio
        ).all()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[AttendancePeriod]:
        """Obtener todos los períodos con paginación."""
        return db.query(AttendancePeriod).offset(skip).limit(limit).all()
    
    def create(self, db: Session, period: AttendancePeriod) -> AttendancePeriod:
        """Crear un nuevo período."""
        db.add(period)
        db.commit()
        db.refresh(period)
        return period
    
    def update(self, db: Session, period: AttendancePeriod) -> AttendancePeriod:
        """Actualizar un período existente."""
        db.commit()
        db.refresh(period)
        return period
    
    def delete(self, db: Session, period: AttendancePeriod) -> None:
        """Eliminar físicamente un período."""
        db.delete(period)
        db.commit()


class AttendanceRepository:
    """
    Repositorio para gestionar asistencias.
    """
    
    def get_by_id(self, db: Session, attendance_id: int) -> Optional[Attendance]:
        """Obtener una asistencia por su ID."""
        return db.query(Attendance).filter(Attendance.id == attendance_id).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[Attendance]:
        """Obtener todas las asistencias con paginación."""
        return db.query(Attendance).offset(skip).limit(limit).all()
    
    def get_by_cooperativista(self, db: Session, cooperativista_id: int) -> List[Attendance]:
        """Obtener todas las asistencias de un cooperativista."""
        return db.query(Attendance).filter(
            Attendance.cooperativista_id == cooperativista_id
        ).order_by(Attendance.fecha.desc(), Attendance.hora.desc()).all()
    
    def get_by_period(self, db: Session, period_id: int) -> List[Attendance]:
        """Obtener todas las asistencias de un período."""
        return db.query(Attendance).filter(Attendance.period_id == period_id).all()
    
    def get_by_cooperativista_and_period(
        self, 
        db: Session, 
        cooperativista_id: int, 
        period_id: int
    ) -> Optional[Attendance]:
        """Obtener la asistencia de un cooperativista en un período específico."""
        return db.query(Attendance).filter(
            Attendance.cooperativista_id == cooperativista_id,
            Attendance.period_id == period_id
        ).first()
    
    def get_by_date(self, db: Session, fecha: date) -> List[Attendance]:
        """Obtener todas las asistencias de una fecha específica."""
        return db.query(Attendance).filter(Attendance.fecha == fecha).all()
    
    def get_by_date_range(self, db: Session, start_date: date, end_date: date) -> List[Attendance]:
        """Obtener asistencias en un rango de fechas."""
        return db.query(Attendance).filter(
            and_(Attendance.fecha >= start_date, Attendance.fecha <= end_date)
        ).all()
    
    def count_by_period(self, db: Session, period_id: int) -> int:
        """Contar asistencias en un período."""
        return db.query(Attendance).filter(Attendance.period_id == period_id).count()
    
    def create(self, db: Session, attendance: Attendance) -> Attendance:
        """Crear una nueva asistencia."""
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        return attendance
    
    def update(self, db: Session, attendance: Attendance) -> Attendance:
        """Actualizar una asistencia existente."""
        db.commit()
        db.refresh(attendance)
        return attendance
    
    def delete(self, db: Session, attendance: Attendance) -> None:
        """Eliminar físicamente una asistencia."""
        db.delete(attendance)
        db.commit()


class AttendanceLogRepository:
    """
    Repositorio para gestionar logs de asistencia.
    """
    
    def get_by_attendance(self, db: Session, attendance_id: int) -> List[AttendanceLog]:
        """Obtener todos los logs de una asistencia, ordenados por fecha."""
        return db.query(AttendanceLog).filter(
            AttendanceLog.attendance_id == attendance_id
        ).order_by(AttendanceLog.created_at.desc()).all()
    
    def create(self, db: Session, log: AttendanceLog) -> AttendanceLog:
        """Crear un nuevo log."""
        db.add(log)
        db.commit()
        db.refresh(log)
        return log


# Instancias de repositorios
attendance_period_repo = AttendancePeriodRepository()
attendance_repo = AttendanceRepository()
attendance_log_repo = AttendanceLogRepository()
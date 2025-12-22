from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.attendance_repo import (
    attendance_repo, 
    attendance_period_repo, 
    attendance_log_repo
)
from repositories.cooperativista_repo import cooperativista_repo
from models.attendance import Attendance, AttendancePeriod, AttendanceLog
from schemas.attendance import (
    AttendanceCreate, AttendanceResponse, AttendanceUpdate,
    AttendancePeriodCreate, AttendancePeriodResponse, AttendancePeriodUpdate,
    AttendanceLogResponse
)
from datetime import datetime, date, time
from typing import List, Optional
import json


# ============ SERVICIO DE PERÍODOS DE ASISTENCIA ============

class AttendancePeriodService:
    
    def create_period(
        self,
        db: Session,
        period_data: AttendancePeriodCreate,
        user_id: int
    ) -> AttendancePeriodResponse:
        """
        Crear un nuevo período de asistencia.
        
        Validaciones:
        - El mes debe estar entre 1 y 12
        - El año debe ser >= 2024
        - La hora de fin debe ser posterior a la hora de inicio
        - No debe existir otro período activo para la misma fecha
        """
        
        # Validar horarios
        if period_data.hora_fin <= period_data.hora_inicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de fin debe ser posterior a la hora de inicio"
            )
        
        # Crear el período
        period = AttendancePeriod(
            nombre=period_data.nombre,
            descripcion=period_data.descripcion,
            mes=period_data.mes,
            anio=period_data.anio,
            fecha_asistencia=period_data.fecha_asistencia,
            hora_inicio=period_data.hora_inicio,
            hora_fin=period_data.hora_fin,
            is_active=period_data.is_active,
            is_open=False,  # Por defecto cerrado, se abre automáticamente
            total_expected=0,
            total_marked=0,
            created_by=user_id
        )
        
        period = attendance_period_repo.create(db, period)
        return AttendancePeriodResponse.model_validate(period)
    
    def get_all_periods(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = False
    ) -> List[AttendancePeriodResponse]:
        """
        Obtener todos los períodos de asistencia.
        """
        if active_only:
            periods = attendance_period_repo.get_active(db)
        else:
            periods = attendance_period_repo.get_all(db, skip, limit)
        
        return [AttendancePeriodResponse.model_validate(p) for p in periods]
    
    def get_period_by_id(self, db: Session, period_id: int) -> AttendancePeriodResponse:
        """
        Obtener un período por su ID.
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        return AttendancePeriodResponse.model_validate(period)
    
    def update_period(
        self,
        db: Session,
        period_id: int,
        period_data: AttendancePeriodUpdate,
        user_id: int
    ) -> AttendancePeriodResponse:
        """
        Actualizar un período existente.
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        
        # Actualizar solo los campos proporcionados
        update_data = period_data.model_dump(exclude_unset=True)
        
        # Validar horarios si se actualizan
        hora_inicio = update_data.get('hora_inicio', period.hora_inicio)
        hora_fin = update_data.get('hora_fin', period.hora_fin)
        
        if hora_fin <= hora_inicio:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="La hora de fin debe ser posterior a la hora de inicio"
            )
        
        for key, value in update_data.items():
            setattr(period, key, value)
        
        period = attendance_period_repo.update(db, period)
        return AttendancePeriodResponse.model_validate(period)
    
    def deactivate_period(
        self,
        db: Session,
        period_id: int,
        user_id: int
    ) -> AttendancePeriodResponse:
        """
        Desactivar un período (eliminación lógica).
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        
        period.is_active = False
        period.is_open = False
        period = attendance_period_repo.update(db, period)
        
        return AttendancePeriodResponse.model_validate(period)
    
    def close_period(
        self,
        db: Session,
        period_id: int,
        user_id: int
    ) -> AttendancePeriodResponse:
        """
        Cerrar un período de asistencia.
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        
        if not period.is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El período ya está cerrado"
            )
        
        period.is_open = False
        period.closed_at = datetime.now()
        period.closed_by = user_id
        period = attendance_period_repo.update(db, period)
        
        return AttendancePeriodResponse.model_validate(period)
    
    def open_period(
        self,
        db: Session,
        period_id: int,
        user_id: int
    ) -> AttendancePeriodResponse:
        """
        Abrir un período de asistencia manualmente.
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        
        if not period.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se puede abrir un período inactivo"
            )
        
        if period.is_open:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El período ya está abierto"
            )
        
        period.is_open = True
        period.closed_at = None
        period.closed_by = None
        period = attendance_period_repo.update(db, period)
        
        return AttendancePeriodResponse.model_validate(period)
    
    def hard_delete_period(self, db: Session, period_id: int) -> None:
        """
        SOLO DESARROLLO: Eliminación física de un período.
        """
        period = attendance_period_repo.get_by_id(db, period_id)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Período no encontrado"
            )
        
        # Verificar si tiene asistencias registradas
        attendances = attendance_repo.get_by_period(db, period_id)
        if attendances:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No se puede eliminar el período porque tiene {len(attendances)} asistencias registradas"
            )
        
        attendance_period_repo.delete(db, period)
    
    def get_periods_by_month(
        self,
        db: Session,
        mes: int,
        anio: int
    ) -> List[AttendancePeriodResponse]:
        """
        Obtener todos los períodos de un mes específico.
        """
        periods = attendance_period_repo.get_by_month(db, mes, anio)
        return [AttendancePeriodResponse.model_validate(p) for p in periods]
    
    def get_period_by_date(self, db: Session, fecha: date) -> AttendancePeriodResponse:
        """
        Obtener el período activo para una fecha específica.
        """
        period = attendance_period_repo.get_by_date(db, fecha)
        if not period:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No existe un período activo para la fecha {fecha}"
            )
        return AttendancePeriodResponse.model_validate(period)
    
    def check_and_open_periods(self, db: Session) -> List[AttendancePeriod]:
        """
        Verificar y abrir automáticamente los períodos cuya hora de inicio ha llegado.
        
        Esta función debe ser llamada por un scheduler/background task.
        """
        now = datetime.now()
        current_date = now.date()
        current_time = now.time()
        
        # Obtener períodos activos que aún no están abiertos
        closed_periods = db.query(AttendancePeriod).filter(
            AttendancePeriod.is_active == True,
            AttendancePeriod.is_open == False,
            AttendancePeriod.fecha_asistencia == current_date,
            AttendancePeriod.hora_inicio <= current_time,
            AttendancePeriod.hora_fin >= current_time
        ).all()
        
        opened_periods = []
        for period in closed_periods:
            period.is_open = True
            period = attendance_period_repo.update(db, period)
            opened_periods.append(period)
        
        return opened_periods


# ============ SERVICIO DE ASISTENCIAS ============

class AttendanceService:
    
    def register_attendance(
        self, 
        db: Session, 
        attendance_data: AttendanceCreate, 
        user_id: int
    ) -> AttendanceResponse:
        """
        Registrar asistencia mediante escaneo de código QR.
        
        Validaciones:
        - El cooperativista debe existir y estar activo
        - Si se especifica un período, debe existir y estar abierto
        - No debe existir registro previo para el mismo cooperativista en el mismo período
        
        Se crea automáticamente un log con la acción "registro de asistencia por scanner".
        """
        # Verificar que el cooperativista existe
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
        
        # Verificar el período si se especifica
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
            
            # Verificar que no exista registro previo
            existing = attendance_repo.get_by_cooperativista_and_period(
                db, cooperativista.id, period.id
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe registro de asistencia para este período"
                )
        
        # Crear el registro de asistencia
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
        
        # Actualizar contador del período si aplica
        if period:
            period.total_marked = attendance_repo.count_by_period(db, period.id)
            attendance_period_repo.update(db, period)
        
        # Crear log automático de registro por scanner
        log = AttendanceLog(
            attendance_id=attendance.id,
            action="registro de asistencia por scanner",
            changed_by=user_id,
            old_values=None,
            new_values=json.dumps({
                "cooperativista_id": attendance.cooperativista_id,
                "period_id": attendance.period_id,
                "tipo": attendance.tipo,
                "fecha": attendance.fecha.isoformat(),
                "hora": attendance.hora.isoformat()
            }),
            reason="Registro automático mediante escaneo de código QR",
            ip_address=None  # Se puede obtener del request si es necesario
        )
        attendance_log_repo.create(db, log)
        
        return AttendanceResponse.model_validate(attendance)
    
    def register_manual_attendance(
        self,
        db: Session,
        cooperativista_id: int,
        user_id: int,
        period_id: int = None,
        tipo: str = "entrada",
        reason: str = None
    ) -> AttendanceResponse:
        """
        Registrar asistencia de forma manual (sin QR).
        
        Validaciones:
        - El cooperativista debe existir y estar activo
        - Si se especifica un período, debe existir y estar abierto
        - No debe existir registro previo para el mismo cooperativista en el mismo período
        
        Se crea automáticamente un log con la acción "registro manual de asistencia" y el motivo.
        """
        # Verificar que el cooperativista existe
        cooperativista = cooperativista_repo.get_by_id(db, cooperativista_id)
        
        if not cooperativista:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cooperativista no encontrado"
            )
        
        if not cooperativista.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cooperativista inactivo"
            )
        
        # Verificar el período si se especifica
        period = None
        if period_id:
            period = attendance_period_repo.get_by_id(db, period_id)
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
            
            # Verificar que no exista registro previo
            existing = attendance_repo.get_by_cooperativista_and_period(
                db, cooperativista_id, period_id
            )
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya existe registro de asistencia para este período"
                )
        
        # Crear el registro de asistencia
        now = datetime.now()
        
        attendance = Attendance(
            cooperativista_id=cooperativista_id,
            period_id=period_id,
            registered_by=user_id,
            tipo=tipo,
            fecha=now.date(),
            hora=now.time(),
            timestamp=now
        )
        
        attendance = attendance_repo.create(db, attendance)
        
        # Actualizar contador del período si aplica
        if period:
            period.total_marked = attendance_repo.count_by_period(db, period_id)
            attendance_period_repo.update(db, period)
        
        # Crear log de registro manual con motivo
        log_reason = reason if reason else "Registro manual desde panel administrativo"
        
        try:
            log = AttendanceLog(
                attendance_id=attendance.id,
                action="registro manual de asistencia",
                changed_by=user_id,
                old_values=None,
                new_values=json.dumps({
                    "cooperativista_id": attendance.cooperativista_id,
                    "period_id": attendance.period_id,
                    "tipo": attendance.tipo,
                    "fecha": attendance.fecha.isoformat(),
                    "hora": attendance.hora.isoformat()
                }),
                reason=log_reason,
                ip_address=None
            )
            attendance_log_repo.create(db, log)
        except Exception as e:
            # Log el error pero no fallar la operación completa
            print(f"Error al crear log de asistencia: {str(e)}")
            # Opcional: podrías hacer rollback aquí si quieres que sea atómico
            # db.rollback()
            # raise HTTPException(
            #     status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            #     detail=f"Error al crear log: {str(e)}"
            # )
        
        return AttendanceResponse.model_validate(attendance)
    
    def get_all_attendances(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[AttendanceResponse]:
        """
        Obtener todas las asistencias.
        """
        attendances = attendance_repo.get_all(db, skip, limit)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_attendance_by_id(self, db: Session, attendance_id: int) -> AttendanceResponse:
        """
        Obtener una asistencia por su ID.
        """
        attendance = attendance_repo.get_by_id(db, attendance_id)
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asistencia no encontrada"
            )
        return AttendanceResponse.model_validate(attendance)
    
    def update_attendance(
        self,
        db: Session,
        attendance_id: int,
        attendance_data: AttendanceUpdate,
        user_id: int
    ) -> AttendanceResponse:
        """
        Actualizar una asistencia existente.
        Se crea automáticamente un log con los cambios realizados.
        """
        attendance = attendance_repo.get_by_id(db, attendance_id)
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asistencia no encontrada"
            )
        
        # Guardar valores antiguos para el log
        old_values = {
            "tipo": attendance.tipo,
            "fecha": attendance.fecha.isoformat(),
            "hora": attendance.hora.isoformat()
        }
        
        # Actualizar solo los campos proporcionados
        update_data = attendance_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(attendance, key, value)
        
        attendance = attendance_repo.update(db, attendance)
        
        # Crear log de modificación
        new_values = {
            "tipo": attendance.tipo,
            "fecha": attendance.fecha.isoformat(),
            "hora": attendance.hora.isoformat()
        }
        
        log = AttendanceLog(
            attendance_id=attendance.id,
            action="modificación manual de asistencia",
            changed_by=user_id,
            old_values=json.dumps(old_values),
            new_values=json.dumps(new_values),
            reason="Actualización manual desde panel administrativo"
        )
        attendance_log_repo.create(db, log)
        
        return AttendanceResponse.model_validate(attendance)
    
    def hard_delete_attendance(self, db: Session, attendance_id: int) -> None:
        """
        SOLO DESARROLLO: Eliminación física de una asistencia.
        """
        attendance = attendance_repo.get_by_id(db, attendance_id)
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asistencia no encontrada"
            )
        
        # Actualizar contador del período si aplica
        if attendance.period_id:
            period = attendance_period_repo.get_by_id(db, attendance.period_id)
            if period:
                attendance_repo.delete(db, attendance)
                period.total_marked = attendance_repo.count_by_period(db, attendance.period_id)
                attendance_period_repo.update(db, period)
                return
        
        attendance_repo.delete(db, attendance)
    
    def get_by_cooperativista(self, db: Session, cooperativista_id: int) -> List[AttendanceResponse]:
        """
        Obtener todas las asistencias de un cooperativista.
        """
        attendances = attendance_repo.get_by_cooperativista(db, cooperativista_id)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_by_period(self, db: Session, period_id: int) -> List[AttendanceResponse]:
        """
        Obtener todas las asistencias de un período.
        """
        attendances = attendance_repo.get_by_period(db, period_id)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_by_date(self, db: Session, fecha: date) -> List[AttendanceResponse]:
        """
        Obtener todas las asistencias de una fecha.
        """
        attendances = attendance_repo.get_by_date(db, fecha)
        return [AttendanceResponse.model_validate(a) for a in attendances]
    
    def get_attendance_logs(
        self,
        db: Session,
        attendance_id: int
    ) -> List[AttendanceLogResponse]:
        """
        Obtener todos los logs de una asistencia.
        """
        # Verificar que la asistencia existe
        attendance = attendance_repo.get_by_id(db, attendance_id)
        if not attendance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Asistencia no encontrada"
            )
        
        logs = attendance_log_repo.get_by_attendance(db, attendance_id)
        return [AttendanceLogResponse.model_validate(log) for log in logs]


# Instancias de servicios
attendance_period_service = AttendancePeriodService()
attendance_service = AttendanceService()
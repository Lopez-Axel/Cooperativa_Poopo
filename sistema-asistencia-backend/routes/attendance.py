from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import date
from utils.dependencies import get_db, get_current_user
from services.attendance_service import attendance_service, attendance_period_service
from schemas.attendance import (
    AttendanceCreate, AttendanceResponse, AttendanceUpdate,
    AttendancePeriodCreate, AttendancePeriodResponse, AttendancePeriodUpdate,
    AttendanceLogResponse
)

router = APIRouter(prefix="/attendance", tags=["Attendance"])

# ============ ENDPOINTS DE PERÍODOS DE ASISTENCIA ============

@router.post("/periods", response_model=AttendancePeriodResponse, status_code=status.HTTP_201_CREATED)
def create_period(
    period_data: AttendancePeriodCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Crear un nuevo período de asistencia.
    
    - **nombre**: Nombre descriptivo del período
    - **mes**: Mes del período (1-12)
    - **anio**: Año del período (>=2024)
    - **fecha_asistencia**: Fecha en la que se registrarán las asistencias
    - **hora_inicio**: Hora de inicio del período
    - **hora_fin**: Hora de fin del período
    """
    return attendance_period_service.create_period(db, period_data, current_user.id)


@router.get("/periods", response_model=List[AttendancePeriodResponse])
def get_all_periods(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todos los períodos de asistencia.
    
    - **skip**: Número de registros a omitir (paginación)
    - **limit**: Número máximo de registros a retornar
    - **active_only**: Si es True, solo retorna períodos activos
    """
    return attendance_period_service.get_all_periods(db, skip, limit, active_only)


@router.get("/periods/{period_id}", response_model=AttendancePeriodResponse)
def get_period_by_id(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener el detalle de un período específico por su ID.
    """
    return attendance_period_service.get_period_by_id(db, period_id)


@router.put("/periods/{period_id}", response_model=AttendancePeriodResponse)
def update_period(
    period_id: int,
    period_data: AttendancePeriodUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Actualizar un período de asistencia existente.
    """
    return attendance_period_service.update_period(db, period_id, period_data, current_user.id)


@router.delete("/periods/{period_id}/deactivate", response_model=AttendancePeriodResponse)
def deactivate_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Desactivar un período (eliminación lógica).
    Establece is_active = False sin eliminar el registro.
    """
    return attendance_period_service.deactivate_period(db, period_id, current_user.id)


@router.delete("/periods/{period_id}/hard-delete")
def hard_delete_period(
    period_id: int,
    confirm: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    SOLO DESARROLLO: Eliminación física de un período.
    Requiere confirmación explícita con confirm="DELETE_PERMANENTLY"
    """
    if confirm != "DELETE_PERMANENTLY":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe confirmar la eliminación física con confirm='DELETE_PERMANENTLY'"
        )
    
    attendance_period_service.hard_delete_period(db, period_id)
    return {"message": "Período eliminado permanentemente"}


@router.post("/periods/{period_id}/close", response_model=AttendancePeriodResponse)
def close_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Cerrar un período de asistencia.
    Establece is_open = False e impide nuevos registros de asistencia.
    """
    return attendance_period_service.close_period(db, period_id, current_user.id)


@router.post("/periods/{period_id}/open", response_model=AttendancePeriodResponse)
def open_period(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Abrir un período de asistencia manualmente.
    Útil para períodos fuera de tiempo o cuando el scheduler no funciona.
    """
    return attendance_period_service.open_period(db, period_id, current_user.id)


@router.get("/periods/month/{year}/{month}", response_model=List[AttendancePeriodResponse])
def get_periods_by_month(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todos los períodos de un mes específico.
    """
    return attendance_period_service.get_periods_by_month(db, month, year)


@router.get("/periods/date/{fecha}", response_model=AttendancePeriodResponse)
def get_period_by_date(
    fecha: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener el período activo para una fecha específica.
    """
    return attendance_period_service.get_period_by_date(db, fecha)


@router.post("/periods/check-and-open")
def check_and_open_periods(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    UTILIDAD: Verificar y abrir manualmente los períodos que deberían estar abiertos.
    Útil si el scheduler automático no está funcionando.
    """
    opened = attendance_period_service.check_and_open_periods(db)
    return {
        "message": f"Se verificaron los períodos. {len(opened)} período(s) abierto(s).",
        "opened_periods": [AttendancePeriodResponse.model_validate(p) for p in opened]
    }


# ============ ENDPOINTS DE ASISTENCIAS ============

@router.post("/scan", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def register_attendance(
    attendance_data: AttendanceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Registrar asistencia mediante escaneo de código QR.
    
    - **qr_code**: Código QR del cooperativista
    - **period_id**: ID del período (opcional)
    - **tipo**: Tipo de registro ("entrada" o "salida")
    
    Se crea automáticamente un log con la acción "registro de asistencia por scanner".
    """
    return attendance_service.register_attendance(db, attendance_data, current_user.id)


@router.post("/manual", response_model=AttendanceResponse, status_code=status.HTTP_201_CREATED)
def register_manual_attendance(
    attendance_data: dict,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Registrar asistencia de forma manual (sin QR).
    
    - **cooperativista_id**: ID del cooperativista
    - **period_id**: ID del período (opcional)
    - **tipo**: Tipo de registro ("entrada" o "salida", por defecto "entrada")
    - **reason**: Motivo del registro manual (falta de credencial, registro tardío, etc.)
    
    Se crea automáticamente un log con la acción "registro manual de asistencia" y el motivo.
    """
    return attendance_service.register_manual_attendance(
        db, 
        attendance_data.get('cooperativista_id'), 
        current_user.id, 
        attendance_data.get('period_id'), 
        attendance_data.get('tipo', 'entrada'), 
        attendance_data.get('reason')
    )


@router.get("/", response_model=List[AttendanceResponse])
def get_all_attendances(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todas las asistencias registradas.
    """
    return attendance_service.get_all_attendances(db, skip, limit)


@router.get("/{attendance_id}", response_model=AttendanceResponse)
def get_attendance_by_id(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener el detalle de una asistencia específica por su ID.
    """
    return attendance_service.get_attendance_by_id(db, attendance_id)


@router.put("/{attendance_id}", response_model=AttendanceResponse)
def update_attendance(
    attendance_id: int,
    attendance_data: AttendanceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Actualizar una asistencia existente.
    Se crea automáticamente un log con los cambios realizados.
    """
    return attendance_service.update_attendance(db, attendance_id, attendance_data, current_user.id)


@router.delete("/{attendance_id}/hard-delete")
def hard_delete_attendance(
    attendance_id: int,
    confirm: str = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    SOLO DESARROLLO: Eliminación física de una asistencia.
    Requiere confirmación explícita con confirm="DELETE_PERMANENTLY"
    """
    if confirm != "DELETE_PERMANENTLY":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debe confirmar la eliminación física con confirm='DELETE_PERMANENTLY'"
        )
    
    attendance_service.hard_delete_attendance(db, attendance_id)
    return {"message": "Asistencia eliminada permanentemente"}


@router.get("/cooperativista/{cooperativista_id}", response_model=List[AttendanceResponse])
def get_cooperativista_attendance(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todas las asistencias de un cooperativista específico.
    """
    return attendance_service.get_by_cooperativista(db, cooperativista_id)


@router.get("/period/{period_id}", response_model=List[AttendanceResponse])
def get_period_attendance(
    period_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todas las asistencias de un período específico.
    """
    return attendance_service.get_by_period(db, period_id)


@router.get("/date/{fecha}", response_model=List[AttendanceResponse])
def get_date_attendance(
    fecha: date,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todas las asistencias de una fecha específica.
    """
    return attendance_service.get_by_date(db, fecha)


# ============ ENDPOINTS DE LOGS DE ASISTENCIA ============

@router.get("/{attendance_id}/logs", response_model=List[AttendanceLogResponse])
def get_attendance_logs(
    attendance_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Obtener todos los logs asociados a una asistencia específica.
    
    Los logs registran todas las acciones realizadas sobre una asistencia:
    - Registro inicial por scanner
    - Modificaciones manuales
    - Correcciones administrativas
    """
    return attendance_service.get_attendance_logs(db, attendance_id)
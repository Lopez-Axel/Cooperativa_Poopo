from .user_repo import user_repo
from .device_repo import device_repo
from .seccion_repo import seccion_repo
from .cuadrilla_repo import cuadrilla_repo
from .cooperativista_repo import cooperativista_repo
from .attendance_repo import attendance_period_repo, attendance_repo, attendance_log_repo

__all__ = [
    "user_repo",
    "device_repo",
    "seccion_repo",
    "cuadrilla_repo",
    "cooperativista_repo",
    "attendance_period_repo",
    "attendance_repo",
    "attendance_log_repo",
]
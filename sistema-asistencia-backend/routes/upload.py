from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from utils.dependencies import get_db, get_current_user
from services.upload_service import upload_service

router = APIRouter(prefix="/uploads", tags=["Uploads"])

@router.post("/cooperativistas/{cooperativista_id}/ci-foto")
async def upload_ci_foto(
    cooperativista_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await upload_service.upload_ci_foto(db, cooperativista_id, file)

@router.post("/cooperativistas/{cooperativista_id}/documento-abc")
async def upload_documento_abc(
    cooperativista_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return await upload_service.upload_documento_abc(db, cooperativista_id, file)

@router.delete("/cooperativistas/{cooperativista_id}/ci-foto")
def delete_ci_foto(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return upload_service.delete_ci_foto(db, cooperativista_id)

@router.delete("/cooperativistas/{cooperativista_id}/documento-abc")
def delete_documento_abc(
    cooperativista_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return upload_service.delete_documento_abc(db, cooperativista_id)
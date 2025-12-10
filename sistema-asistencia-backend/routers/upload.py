from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.cooperativista import Cooperativista
from cloudinary import uploader
import os
import mimetypes

router = APIRouter(prefix="/uploads", tags=["uploads"])

ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp"}
ALLOWED_DOC_TYPES = {"application/pdf", "image/jpeg", "image/jpg", "image/png"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_DOC_SIZE = 20 * 1024 * 1024    # 20MB

@router.post("/cooperativistas/{cooperativista_id}/ci-foto")
async def upload_ci_foto(
    cooperativista_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG, WEBP")
    
    contents = await file.read()
    if len(contents) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Imagen muy pesada (máx 10MB)")
    
    try:
        result = uploader.upload(
            contents,
            folder="cooperativa/ci_fotos",
            public_id=f"ci_{cooperativista_id}",
            overwrite=True,
            resource_type="image",
            transformation=[
                {"width": 1200, "height": 1200, "crop": "limit"},
                {"quality": "auto:good"}
            ]
        )
        
        coop.ci_foto_url = result['secure_url']
        db.commit()
        
        return {
            "message": "Foto de CI subida exitosamente",
            "url": result['secure_url']
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir imagen: {str(e)}")

@router.post("/cooperativistas/{cooperativista_id}/documento-abc")
async def upload_documento_abc(
    cooperativista_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if file.content_type not in ALLOWED_DOC_TYPES:
        raise HTTPException(status_code=400, detail="Solo se permiten PDF o imágenes")
    
    # tamaño: usa seek/tell si trabajas con file.file, o ya con .read() como antes
    contents = await file.read()
    if len(contents) > MAX_DOC_SIZE:
        raise HTTPException(status_code=400, detail="Archivo muy pesado (máx 20MB)")
    # rewind file if we want to pass file.file to uploader
    try:
        # determinar extensión segura (preferir filename si existe)
        filename = getattr(file, "filename", None) or "file"
        ext = filename.split(".")[-1].lower() if "." in filename else None
        if not ext:
            # mapear desde content_type
            ext = mimetypes.guess_extension(file.content_type) or ""
            ext = ext.lstrip(".")
        
        # elegir resource_type
        if file.content_type.startswith("image/"):
            resource_type = "image"
            upload_kwargs = {
                "folder": "cooperativa/documentos_abc",
                "public_id": f"doc_abc_{cooperativista_id}",
                "overwrite": True,
                "resource_type": resource_type,
            }
            result = uploader.upload(contents, **upload_kwargs)
        else:
            resource_type = "raw"
            upload_kwargs = {
                "folder": "cooperativa/documentos_abc",
                "public_id": f"doc_abc_{cooperativista_id}",
                "overwrite": True,
                "resource_type": resource_type,
                "format": ext if ext else "pdf",
            }

            result = uploader.upload(contents, **upload_kwargs)
        
        coop.documento_abc_url = result.get('secure_url') or result.get('url')
        coop.documento_abc_public_id = result.get('public_id')  # opcional: guarda public_id
        db.commit()
        
        return {
            "message": "Documento ABC subido exitosamente",
            "url": coop.documento_abc_url,
            "result": {
                "format": result.get("format"),
                "resource_type": result.get("resource_type"),
                "public_id": result.get("public_id"),
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al subir documento: {str(e)}")
    
@router.delete("/cooperativistas/{cooperativista_id}/ci-foto")
def delete_ci_foto(cooperativista_id: int, db: Session = Depends(get_db)):
    coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if not coop.ci_foto_url:
        raise HTTPException(status_code=404, detail="No hay foto de CI")
    
    coop.ci_foto_url = None
    db.commit()
    
    return {"message": "Foto de CI eliminada"}

@router.delete("/cooperativistas/{cooperativista_id}/documento-abc")
def delete_documento_abc(cooperativista_id: int, db: Session = Depends(get_db)):
    coop = db.query(Cooperativista).filter(Cooperativista.id == cooperativista_id).first()
    if not coop:
        raise HTTPException(status_code=404, detail="Cooperativista no encontrado")
    
    if not coop.documento_abc_url:
        raise HTTPException(status_code=404, detail="No hay documento ABC")
    
    coop.documento_abc_url = None
    db.commit()
    
    return {"message": "Documento ABC eliminado"}
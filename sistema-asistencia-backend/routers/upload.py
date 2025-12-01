from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from database import get_db
from models.cooperativista import Cooperativista
from cloudinary import uploader
import os

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
    
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.utils import cloudinary_url

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
    
    contents = await file.read()
    if len(contents) > MAX_DOC_SIZE:
        raise HTTPException(status_code=400, detail="Archivo muy pesado (máx 20MB)")

    # Conserva el nombre original (útil para descarga)
    original_filename = file.filename or f"doc_abc_{cooperativista_id}"
    # Extraer extensión (por si la quieres usar)
    ext = original_filename.split(".")[-1].lower() if "." in original_filename else None

    try:
        # Para imágenes sigue siendo resource_type="image", para PDF/Otros -> "raw"
        is_image = file.content_type.startswith("image/")
        resource_type = "image" if is_image else "raw"

        # Si es raw (pdf), usamos el file.file (file-like) y forzamos format si es pdf
        upload_args = dict(
            folder="cooperativa/documentos_abc",
            public_id=f"doc_abc_{cooperativista_id}",
            overwrite=True,
            resource_type=resource_type,
            use_filename=True,        # intenta mantener el nombre original
            unique_filename=False     # evita que Cloudinary agregue sufijos extra
        )

        # Si sabemos que es PDF, fuerza el formato pdf (esto hace que Cloudinary guarde el formato)
        if not is_image and (file.content_type == "application/pdf" or ext == "pdf"):
            upload_args["format"] = "pdf"

        result = cloudinary_upload(contents, **upload_args)

        # result habitualmente trae 'public_id' y 'format' (ej: 'pdf')
        public_id = result.get("public_id")
        saved_format = result.get("format") or ext or "bin"

        # Generar una URL de descarga que forzará el nombre y extensión con la transformación `attachment`
        download_name = f"{original_filename}" if original_filename.lower().endswith(saved_format) else f"{original_filename}.{saved_format}"
        download_url, _ = cloudinary_url(
            public_id,
            resource_type=resource_type,
            format=saved_format,
            attachment=download_name,  # fuerza Content-Disposition: attachment; filename="..."
            secure=True
        )

        # Guarda URL de descarga (contendrá los parámetros para forzar descarga con nombre)
        coop.documento_abc_url = download_url
        db.commit()
        
        return {
            "message": "Documento ABC subido exitosamente",
            "url": download_url,
            "public_id": public_id,
            "format": saved_format
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
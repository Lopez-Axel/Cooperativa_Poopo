from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from database import get_db
from models.user import User
from schemas.token import Token, LoginRequest
from utils.security import verify_password
from utils.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint de inicio de sesión
    
    Proceso:
    1. Valida que el usuario existe
    2. Verifica la contraseña con bcrypt
    3. Verifica que el usuario esté activo
    4. Genera un JWT firmado con los datos del usuario
    5. Actualiza last_login en la base de datos
    6. Devuelve el token y datos del usuario
    
    Args:
        credentials: Username y password
        db: Sesión de base de datos
        
    Returns:
        Token JWT y datos del usuario
        
    Raises:
        HTTPException 401: Si las credenciales son incorrectas
        HTTPException 403: Si el usuario está inactivo
    """
    # Buscar usuario por username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar contraseña
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo. Contacte al administrador."
        )
    
    # Actualizar last_login
    user.last_login = datetime.utcnow()
    db.commit()
    
    # Crear el payload del JWT
    token_data = {
        "sub": str(user.id),  # Subject: ID del usuario
        "username": user.username,
        "is_superuser": user.is_superuser,
        "is_active": user.is_active
    }
    
    # Generar el token JWT
    access_token = create_access_token(data=token_data)
    
    # Devolver respuesta
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "is_superuser": user.is_superuser,
            "is_active": user.is_active
        }
    }


@router.post("/logout")
def logout():
    """
    Endpoint de cierre de sesión
    
    Nota: Con JWT stateless, el logout se maneja en el cliente
    eliminando el token del localStorage. Este endpoint es
    principalmente informativo o para futuras implementaciones
    (como blacklist de tokens).
    """
    return {
        "message": "Sesión cerrada correctamente",
        "detail": "Elimina el token del cliente para completar el logout"
    }
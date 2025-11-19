from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from database import get_db
from models.user import User
from utils.jwt import decode_access_token

# Configuración de seguridad Bearer Token
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency que valida el JWT y devuelve el usuario actual
    
    Se ejecuta ANTES del endpoint para:
    1. Extraer el token del header Authorization
    2. Validar la firma del JWT
    3. Verificar que no haya expirado
    4. Buscar el usuario en la base de datos
    5. Verificar que esté activo
    
    Uso en endpoints:
        @router.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            # Si llegas aquí, el usuario está autenticado
            return {"user": current_user.username}
    
    Args:
        credentials: Token extraído del header Authorization: Bearer <token>
        db: Sesión de base de datos
        
    Returns:
        Usuario autenticado
        
    Raises:
        HTTPException 401: Si el token es inválido, expirado o el usuario no existe
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extraer el token
    token = credentials.credentials
    
    # Decodificar y validar el token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extraer el user_id del token
    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise credentials_exception
    
    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Verificar que el usuario esté activo
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency que verifica que el usuario sea superadmin
    
    Usa get_current_user primero (autenticación) y luego
    verifica que tenga privilegios de superusuario (autorización)
    
    Uso en endpoints:
        @router.delete("/users/{id}")
        def delete_user(
            id: int,
            current_user: User = Depends(get_current_superuser)
        ):
            # Solo superadmins pueden ejecutar este endpoint
            ...
    
    Args:
        current_user: Usuario autenticado (inyectado por get_current_user)
        
    Returns:
        Usuario superadmin
        
    Raises:
        HTTPException 403: Si el usuario no es superadmin
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requieren privilegios de superusuario para esta operación"
        )
    return current_user


# Dependency opcional para obtener usuario si existe token
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency opcional que devuelve el usuario si hay token válido,
    o None si no hay token (sin lanzar excepción)
    
    Útil para endpoints públicos que pueden personalizar respuesta
    si el usuario está autenticado
    
    Args:
        credentials: Token opcional
        db: Sesión de base de datos
        
    Returns:
        Usuario si está autenticado, None si no
    """
    if not credentials:
        return None
    
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
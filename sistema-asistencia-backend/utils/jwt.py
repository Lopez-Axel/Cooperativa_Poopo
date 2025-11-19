from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_HOURS


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un token JWT firmado con los datos del usuario
    
    Args:
        data: Diccionario con la información a incluir en el token
              Ejemplo: {"sub": "1", "username": "admin", "is_superuser": True}
        expires_delta: Tiempo de expiración personalizado (opcional)
        
    Returns:
        Token JWT firmado como string
    """
    to_encode = data.copy()
    
    # Calcular tiempo de expiración
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    # Agregar campos estándar del JWT
    to_encode.update({
        "exp": expire,  # Expiración
        "iat": datetime.utcnow()  # Issued at (cuándo se creó)
    })
    
    # Crear el token firmado
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica y valida un token JWT
    
    Args:
        token: Token JWT a decodificar
        
    Returns:
        Diccionario con los datos del token si es válido, None si es inválido
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
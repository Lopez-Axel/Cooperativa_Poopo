from passlib.context import CryptContext

# Configuración de bcrypt para hash de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Genera un hash seguro de la contraseña usando bcrypt
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        Hash de la contraseña
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica si una contraseña coincide con su hash
    
    Args:
        plain_password: Contraseña en texto plano
        hashed_password: Hash almacenado en la base de datos
        
    Returns:
        True si coincide, False si no
    """
    return pwd_context.verify(plain_password, hashed_password)
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración JWT
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("ACCESS_TOKEN_EXPIRE_HOURS", 8))

# Base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cooperativa.db")

# Servidor
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
DEBUG = os.getenv("DEBUG", "True").lower() == "true"

# Validaciones de seguridad
if not SECRET_KEY:
    raise ValueError(
        "❌ ERROR: SECRET_KEY no está configurado en el archivo .env\n"
        "Genera uno con: python3 -c \"import secrets; print(secrets.token_urlsafe(64))\""
    )

if len(SECRET_KEY) < 32:
    raise ValueError(
        "❌ ERROR: SECRET_KEY debe tener al menos 32 caracteres para ser seguro"
    )

print("✅ Configuración cargada correctamente")
print(f"✅ JWT expirará en {ACCESS_TOKEN_EXPIRE_HOURS} horas")
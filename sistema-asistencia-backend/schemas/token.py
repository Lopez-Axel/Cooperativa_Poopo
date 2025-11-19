from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """Respuesta del endpoint de login"""
    access_token: str
    token_type: str
    user: dict


class TokenData(BaseModel):
    """Datos extraídos del token JWT"""
    user_id: Optional[int] = None
    username: Optional[str] = None
    is_superuser: Optional[bool] = False


class LoginRequest(BaseModel):
    """Petición de login"""
    username: str
    password: str
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "admin",
                    "password": "admin123"
                }
            ]
        }
    }
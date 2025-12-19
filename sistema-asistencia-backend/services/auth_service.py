from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import timedelta
from repositories.user_repo import user_repo
from repositories.device_repo import device_repo
from utils.security import verify_password, hash_password
from utils.jwt import create_access_token, decode_access_token
from schemas.token import Token

class AuthService:
    
    def login(self, db: Session, username: str, password: str) -> Token:
        user = user_repo.get_by_username(db, username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales incorrectas"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        user_repo.update_last_login(db, user.id)
        
        active_device = device_repo.get_active_by_user(db, user.id)
        
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "is_superuser": user.is_superuser
        }
        access_token = create_access_token(token_data)
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "is_superuser": user.is_superuser,
                "has_active_device": active_device is not None,
                "active_device": {
                    "device_id": active_device.device_id,
                    "device_name": active_device.device_name
                } if active_device else None
            }
        )
    
    def get_current_user(self, db: Session, token: str):
        payload = decode_access_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido"
            )
        
        user = user_repo.get_by_id(db, int(user_id))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado"
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )
        
        return user
    
    def validate_device(self, db: Session, user_id: int, device_id: str) -> bool:
        active_device = device_repo.get_active_by_user(db, user_id)
        
        if not active_device:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No hay dispositivo vinculado"
            )
        
        if active_device.device_id != device_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Dispositivo no autorizado"
            )
        
        device_repo.update_last_seen(db, active_device.id)
        
        return True

auth_service = AuthService()
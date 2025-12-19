from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.user_repo import user_repo
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from utils.security import hash_password
from typing import List

class UserService:
    
    def create_user(self, db: Session, user_data: UserCreate) -> UserResponse:
        if user_repo.get_by_username(db, user_data.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username ya existe"
            )
        
        if user_data.email and user_repo.get_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email ya registrado"
            )
        
        user = User(
            username=user_data.username,
            password_hash=hash_password(user_data.password),
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=user_data.is_active,
            is_superuser=user_data.is_superuser
        )
        
        user = user_repo.create(db, user)
        return UserResponse.model_validate(user)
    
    def get_by_id(self, db: Session, user_id: int) -> UserResponse:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        return UserResponse.model_validate(user)
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = user_repo.get_all(db, skip, limit)
        return [UserResponse.model_validate(u) for u in users]
    
    def update_user(self, db: Session, user_id: int, user_data: UserUpdate) -> UserResponse:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        if user_data.username and user_data.username != user.username:
            if user_repo.get_by_username(db, user_data.username):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username ya existe"
                )
        
        if user_data.email and user_data.email != user.email:
            if user_repo.get_by_email(db, user_data.email):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya registrado"
                )
        
        for field, value in user_data.model_dump(exclude_unset=True).items():
            if field == "password" and value:
                setattr(user, "password_hash", hash_password(value))
            elif field != "password":
                setattr(user, field, value)
        
        user = user_repo.update(db, user)
        return UserResponse.model_validate(user)
    
    def delete_user(self, db: Session, user_id: int) -> dict:
        user = user_repo.get_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        user_repo.delete(db, user)
        return {"message": "Usuario eliminado"}

user_service = UserService()
# routers/users.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserResponse
from utils.security import hash_password
from dependencies.auth import get_current_user, get_current_superuser

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    is_active: Optional[bool] = None,
    is_superuser: Optional[bool] = None,
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),  
    db: Session = Depends(get_db)
):
    """
    Obtener lista de usuarios (requiere autenticación)
    """
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    if is_superuser is not None:
        query = query.filter(User.is_superuser == is_superuser)
    if search:
        query = query.filter(
            (User.username.ilike(f"%{search}%")) |
            (User.full_name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )
    
    return query.offset(skip).limit(limit).all()


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Obtener información del usuario autenticado
    """
    return current_user


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(get_current_user),  # 🔒 Requiere autenticación
    db: Session = Depends(get_db)
):
    """
    Obtener un usuario por ID (requiere autenticación)
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    current_user: User = Depends(get_current_superuser),  # 🔒 Solo superadmin
    db: Session = Depends(get_db)
):
    """
    Crear nuevo usuario (solo superadmin)
    """
    # Verificar que no exista el username
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="El nombre de usuario ya existe"
        )
    
    # Verificar que no exista el email
    if user.email:
        existing_email = db.query(User).filter(User.email == user.email).first()
        if existing_email:
            raise HTTPException(
                status_code=400, 
                detail="El email ya está registrado"
            )
    
    # Crear usuario
    user_data = user.model_dump(exclude={"password"})
    user_data["password_hash"] = hash_password(user.password)
    
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user: UserUpdate,
    current_user: User = Depends(get_current_superuser),  # 🔒 Solo superadmin
    db: Session = Depends(get_db)
):
    """
    Actualizar usuario (solo superadmin)
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Preparar datos a actualizar
    update_data = user.model_dump(exclude_unset=True, exclude={"password"})
    
    # Verificar username único
    if "username" in update_data and update_data["username"] != db_user.username:
        existing = db.query(User).filter(
            User.username == update_data["username"],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="El nombre de usuario ya existe"
            )
    
    # Verificar email único
    if "email" in update_data and update_data["email"]:
        existing = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=400, 
                detail="El email ya está registrado"
            )
    
    # Actualizar password si se proporcionó
    if user.password:
        db_user.password_hash = hash_password(user.password)
    
    # Actualizar demás campos
    for key, value in update_data.items():
        setattr(db_user, key, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_superuser),  # 🔒 Solo superadmin
    db: Session = Depends(get_db)
):
    """
    Eliminar usuario (solo superadmin)
    No permite eliminar el último superusuario
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Prevenir eliminar el último superusuario
    if db_user.is_superuser:
        superusers_count = db.query(User).filter(User.is_superuser == True).count()
        if superusers_count <= 1:
            raise HTTPException(
                status_code=400, 
                detail="No se puede eliminar el último superusuario del sistema"
            )
    
    db.delete(db_user)
    db.commit()


@router.post("/{user_id}/change-password")
def change_password(
    user_id: int,
    old_password: str,
    new_password: str,
    current_user: User = Depends(get_current_user),  # 🔒 Usuario autenticado
    db: Session = Depends(get_db)
):
    """
    Cambiar contraseña (usuario autenticado puede cambiar la suya,
    o superadmin puede cambiar cualquiera)
    """
    # Solo puede cambiar su propia contraseña, a menos que sea superadmin
    if current_user.id != user_id and not current_user.is_superuser:
        raise HTTPException(
            status_code=403,
            detail="No tienes permiso para cambiar esta contraseña"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Verificar contraseña actual (solo si no es superadmin cambiando otra cuenta)
    if current_user.id == user_id:
        from utils.security import verify_password
        if not verify_password(old_password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Contraseña actual incorrecta"
            )
    
    # Actualizar contraseña
    user.password_hash = hash_password(new_password)
    db.commit()
    
    return {"message": "Contraseña actualizada exitosamente"}
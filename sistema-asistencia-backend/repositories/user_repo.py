from sqlalchemy.orm import Session
from sqlalchemy import func
from models.user import User
from typing import Optional, List

class UserRepository:
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()
    
    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> List[User]:
        return db.query(User).offset(skip).limit(limit).all()
    
    def get_active_users(self, db: Session) -> List[User]:
        return db.query(User).filter(User.is_active == True).all()
    
    def create(self, db: Session, user: User) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def update(self, db: Session, user: User) -> User:
        db.commit()
        db.refresh(user)
        return user
    
    def delete(self, db: Session, user: User) -> None:
        db.delete(user)
        db.commit()
    
    def update_last_login(self, db: Session, user_id: int) -> None:
        db.query(User).filter(User.id == user_id).update({"last_login": func.now()})
        db.commit()

user_repo = UserRepository()
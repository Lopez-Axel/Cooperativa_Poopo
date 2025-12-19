from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from utils.dependencies import get_db
from services.auth_service import auth_service
from schemas.token import LoginRequest, Token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login(db, credentials.username, credentials.password)
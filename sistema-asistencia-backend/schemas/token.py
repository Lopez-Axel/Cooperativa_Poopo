from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class TokenData(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    is_superuser: Optional[bool] = False

class LoginRequest(BaseModel):
    username: str
    password: str

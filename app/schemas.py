from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl


class User(BaseModel):
    full_name: str
    email: EmailStr

class UserCreate(User):
    password: str

class UserOut(User):
    id: int
    urls_created: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str 
    jti: str

class TokenData(BaseModel):
    id: Optional[int] = None
    jti: Optional[str] = None

class UrlCreate(BaseModel):
    original: HttpUrl

class UrlOut(BaseModel):
    id: int
    original: HttpUrl
    short: str
    clicks: int
    created_at: datetime

    class Config:
        from_attributes = True
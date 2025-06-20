# app/schemas/user.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "student"

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

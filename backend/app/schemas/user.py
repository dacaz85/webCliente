# app/schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: Optional[str] = 'cliente'
    status: Optional[bool] = False

class UserCreate(UserBase):
    password: str  # password en texto plano para creación

class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    role: Optional[str]
    status: Optional[bool]

class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime]
    last_login: Optional[datetime]

    class Config:
        orm_mode = True

class PasswordAction(BaseModel):
    action: str  # "reset" o "change"
    old_password: Optional[str] = None
    new_password: Optional[str] = None

class LoginRequest(BaseModel):
    email: str
    password: str
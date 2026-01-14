from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreateDTO(BaseModel):
    """DTO para creación de usuario"""
    email: EmailStr
    username: str
    password: str
    full_name: str
    role: str

class UserResponseDTO(BaseModel):
    """DTO para respuesta de usuario"""
    id: int
    email: str
    username: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserUpdateDTO(BaseModel):
    """DTO para actualización de usuario"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
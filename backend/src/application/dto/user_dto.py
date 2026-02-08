from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime


class UserCreateDTO(BaseModel):
    """DTO para creación de usuario"""
    email: EmailStr
    username: str
    password: str
    full_name: str
    role: str
    
    # Campos opcionales según el rol
    phone: Optional[str] = None
    address: Optional[str] = None
    
    # Para médicos
    specialty_id: Optional[int] = None
    license_number: Optional[str] = None
    
    @field_validator('role')
    @classmethod
    def validate_role(cls, v):
        if v not in ['patient', 'doctor', 'admin']:
            raise ValueError('Rol debe ser: patient, doctor o admin')
        return v
    
    @field_validator('specialty_id')
    @classmethod
    def validate_specialty_for_doctor(cls, v, info):
        # Si es médico, specialty_id es obligatorio
        if info.data.get('role') == 'doctor' and not v:
            raise ValueError('specialty_id es obligatorio para médicos')
        return v
    
    @field_validator('license_number')
    @classmethod
    def validate_license_for_doctor(cls, v, info):
        # Si es médico, license_number es obligatorio
        if info.data.get('role') == 'doctor' and not v:
            raise ValueError('license_number es obligatorio para médicos')
        return v


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
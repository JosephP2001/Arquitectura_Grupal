from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AppointmentCreateDTO(BaseModel):
    """DTO para creación de cita"""
    doctor_id: int
    appointment_date: datetime
    reason: str
    duration_minutes: int = 30

class AppointmentResponseDTO(BaseModel):
    """DTO para respuesta de cita"""
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    duration_minutes: int
    status: str
    reason: str
    notes: Optional[str] = None
    
    class Config:
        from_attributes = True

class AppointmentUpdateDTO(BaseModel):
    """DTO para actualización de cita"""
    appointment_date: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None
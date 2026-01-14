from pydantic import BaseModel
from typing import Optional
from datetime import time

class ScheduleCreateDTO(BaseModel):
    """DTO para creación de horario"""
    doctor_id: int
    day_of_week: int  # 0=Lunes, 6=Domingo
    start_time: time
    end_time: time
    is_active: bool = True

class ScheduleResponseDTO(BaseModel):
    """DTO para respuesta de horario"""
    id: int
    doctor_id: int
    day_of_week: int
    start_time: time
    end_time: time
    is_active: bool
    
    class Config:
        from_attributes = True

class ScheduleUpdateDTO(BaseModel):
    """DTO para actualización de horario"""
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    is_active: Optional[bool] = None
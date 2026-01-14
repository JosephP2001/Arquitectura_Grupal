"""
Entidad de dominio: Schedule
Representa un horario de atención médica con sus reglas de negocio
"""
from typing import Optional
from datetime import time, datetime, timedelta

class ScheduleEntity:
    """Entidad de dominio para Horario"""
    
    DAYS_OF_WEEK = {
        0: "Lunes",
        1: "Martes",
        2: "Miércoles",
        3: "Jueves",
        4: "Viernes",
        5: "Sábado",
        6: "Domingo"
    }
    
    def __init__(
        self,
        id: Optional[int],
        doctor_id: int,
        day_of_week: int,
        start_time: time,
        end_time: time,
        is_active: bool = True
    ):
        self.id = id
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = is_active
    
    def get_day_name(self) -> str:
        """Obtiene el nombre del día"""
        return self.DAYS_OF_WEEK.get(self.day_of_week, "Desconocido")
    
    def get_duration_hours(self) -> float:
        """Calcula la duración del horario en horas"""
        start_datetime = datetime.combine(datetime.today(), self.start_time)
        end_datetime = datetime.combine(datetime.today(), self.end_time)
        duration = end_datetime - start_datetime
        return duration.total_seconds() / 3600
    
    def is_time_in_range(self, check_time: time) -> bool:
        """Verifica si una hora está dentro del horario"""
        return self.start_time <= check_time <= self.end_time
    
    def conflicts_with(self, other: 'ScheduleEntity') -> bool:
        """Verifica si hay conflicto con otro horario del mismo día"""
        if self.day_of_week != other.day_of_week:
            return False
        
        return (self.start_time < other.end_time) and (other.start_time < self.end_time)
    
    def validate(self) -> tuple[bool, str]:
        """Valida que el horario sea correcto"""
        # Validar día de la semana
        if not 0 <= self.day_of_week <= 6:
            return False, "Día de la semana inválido"
        
        # Validar que la hora de fin sea después de la hora de inicio
        if self.end_time <= self.start_time:
            return False, "La hora de fin debe ser posterior a la hora de inicio"
        
        # Validar horarios laborales razonables (6 AM a 10 PM)
        if self.start_time < time(6, 0) or self.end_time > time(22, 0):
            return False, "El horario debe estar entre 6:00 AM y 10:00 PM"
        
        return True, "Horario válido"
    
    def __repr__(self):
        return f"<ScheduleEntity(id={self.id}, day={self.get_day_name()}, {self.start_time}-{self.end_time})>"
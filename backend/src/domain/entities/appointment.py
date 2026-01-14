"""
Entidad de dominio: Appointment
Representa una cita médica con sus reglas de negocio
"""
from datetime import datetime, timedelta
from typing import Optional

class AppointmentEntity:
    """Entidad de dominio para Cita Médica"""
    
    def __init__(
        self,
        id: Optional[int],
        patient_id: int,
        doctor_id: int,
        appointment_date: datetime,
        duration_minutes: int = 30,
        status: str = "pending",
        reason: str = "",
        notes: Optional[str] = None
    ):
        self.id = id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date = appointment_date
        self.duration_minutes = duration_minutes
        self.status = status
        self.reason = reason
        self.notes = notes
    
    def get_end_time(self) -> datetime:
        """Calcula la hora de fin de la cita"""
        return self.appointment_date + timedelta(minutes=self.duration_minutes)
    
    def is_pending(self) -> bool:
        """Verifica si la cita está pendiente"""
        return self.status == "pending"
    
    def is_confirmed(self) -> bool:
        """Verifica si la cita está confirmada"""
        return self.status == "confirmed"
    
    def is_completed(self) -> bool:
        """Verifica si la cita fue completada"""
        return self.status == "completed"
    
    def is_cancelled(self) -> bool:
        """Verifica si la cita fue cancelada"""
        return self.status == "cancelled"
    
    def confirm(self):
        """Confirmar la cita"""
        if self.is_pending():
            self.status = "confirmed"
    
    def cancel(self):
        """Cancelar la cita"""
        if not self.is_completed():
            self.status = "cancelled"
    
    def complete(self):
        """Marcar cita como completada"""
        if self.is_confirmed():
            self.status = "completed"
    
    def is_past(self) -> bool:
        """Verifica si la cita ya pasó"""
        return self.appointment_date < datetime.utcnow()
    
    def conflicts_with(self, other: 'AppointmentEntity') -> bool:
        """Verifica si hay conflicto de horario con otra cita"""
        if self.doctor_id != other.doctor_id:
            return False
        
        self_start = self.appointment_date
        self_end = self.get_end_time()
        other_start = other.appointment_date
        other_end = other.get_end_time()
        
        return (self_start < other_end) and (other_start < self_end)
    
    def __repr__(self):
        return f"<AppointmentEntity(id={self.id}, patient={self.patient_id}, doctor={self.doctor_id}, status={self.status})>"
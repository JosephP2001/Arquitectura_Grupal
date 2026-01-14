from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.infrastructure.models.postgresql.models import Appointment

class IAppointmentDAO(ABC):
    """Interface para Appointment DAO"""
    
    @abstractmethod
    def create(self, appointment: Appointment) -> Appointment:
        """Crear una nueva cita"""
        pass
    
    @abstractmethod
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Obtener cita por ID"""
        pass
    
    @abstractmethod
    def get_by_patient(self, patient_id: int) -> List[Appointment]:
        """Obtener citas de un paciente"""
        pass
    
    @abstractmethod
    def get_by_doctor(self, doctor_id: int) -> List[Appointment]:
        """Obtener citas de un médico"""
        pass
    
    @abstractmethod
    def get_by_date_range(
        self,
        doctor_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Appointment]:
        """Obtener citas en un rango de fechas"""
        pass
    
    @abstractmethod
    def update(self, appointment: Appointment) -> Appointment:
        """Actualizar cita"""
        pass
    
    @abstractmethod
    def delete(self, appointment_id: int) -> bool:
        """Eliminar cita"""
        pass
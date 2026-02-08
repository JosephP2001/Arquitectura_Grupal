from abc import ABC, abstractmethod
from typing import Optional, List
from datetime import datetime
from src.infrastructure.models.postgresql.models import Appointment


class IAppointmentDAO(ABC):
    """Interface para Appointment DAO"""

    @abstractmethod
    def create(self, appointment: Appointment) -> Appointment:
        pass

    @abstractmethod
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        pass

    @abstractmethod
    def get_by_patient(self, patient_id: int) -> List[Appointment]:
        pass

    @abstractmethod
    def get_by_doctor(self, doctor_id: int) -> List[Appointment]:
        pass

    @abstractmethod
    def get_by_date_range(
        self, 
        doctor_id: int, 
        start_date: datetime, 
        end_date: datetime
    ) -> List[Appointment]:
        pass

    @abstractmethod
    def update(self, appointment: Appointment) -> Appointment:
        pass

    @abstractmethod
    def delete(self, appointment_id: int) -> bool:
        pass
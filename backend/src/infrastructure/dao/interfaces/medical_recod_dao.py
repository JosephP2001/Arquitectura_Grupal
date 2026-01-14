from abc import ABC, abstractmethod
from typing import Optional, List

class IMedicalRecordDAO(ABC):
    """Interface para Medical Record DAO (MongoDB)"""
    
    @abstractmethod
    def create(self, record: dict) -> str:
        """Crear un nuevo registro médico"""
        pass
    
    @abstractmethod
    def get_by_id(self, record_id: str) -> Optional[dict]:
        """Obtener registro por ID"""
        pass
    
    @abstractmethod
    def get_by_patient(self, patient_id: int) -> List[dict]:
        """Obtener registros de un paciente"""
        pass
    
    @abstractmethod
    def get_by_appointment(self, appointment_id: int) -> Optional[dict]:
        """Obtener registro por cita"""
        pass
    
    @abstractmethod
    def update(self, record_id: str, update_data: dict) -> bool:
        """Actualizar registro médico"""
        pass
    
    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Eliminar registro médico"""
        pass
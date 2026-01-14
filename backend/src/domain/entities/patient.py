"""
Entidad de dominio: Patient
Representa un paciente con sus reglas de negocio
"""
from typing import Optional
from datetime import datetime

class PatientEntity:
    """Entidad de dominio para Paciente"""
    
    def __init__(
        self,
        id: Optional[int],
        user_id: int,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        date_of_birth: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.phone = phone
        self.address = address
        self.date_of_birth = date_of_birth
    
    def get_age(self) -> Optional[int]:
        """Calcula la edad del paciente"""
        if not self.date_of_birth:
            return None
        
        today = datetime.utcnow()
        age = today.year - self.date_of_birth.year
        
        # Ajustar si no ha cumplido años este año
        if (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day):
            age -= 1
        
        return age
    
    def is_minor(self) -> bool:
        """Verifica si el paciente es menor de edad"""
        age = self.get_age()
        return age < 18 if age is not None else False
    
    def __repr__(self):
        return f"<PatientEntity(id={self.id}, user_id={self.user_id})>"
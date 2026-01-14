"""
Entidad de dominio: Doctor
Representa un médico con sus reglas de negocio
"""
from typing import Optional, List

class DoctorEntity:
    """Entidad de dominio para Médico"""
    
    def __init__(
        self,
        id: Optional[int],
        user_id: int,
        specialty_id: int,
        license_number: str,
        phone: Optional[str] = None
    ):
        self.id = id
        self.user_id = user_id
        self.specialty_id = specialty_id
        self.license_number = license_number
        self.phone = phone
    
    def is_available_on_day(self, day_of_week: int, schedules: List) -> bool:
        """Verifica si el médico atiende en un día específico"""
        return any(
            schedule.day_of_week == day_of_week and schedule.is_active
            for schedule in schedules
        )
    
    def validate_license(self) -> bool:
        """Valida formato de número de licencia"""
        # Regla de negocio: Licencia debe tener formato MD-XXX
        return self.license_number.startswith("MD-") and len(self.license_number) >= 6
    
    def __repr__(self):
        return f"<DoctorEntity(id={self.id}, license={self.license_number})>"
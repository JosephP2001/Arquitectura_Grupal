"""
Entidad de dominio: User
Representa un usuario del sistema con sus reglas de negocio
"""
from datetime import datetime
from typing import Optional

class UserEntity:
    """Entidad de dominio para Usuario"""
    
    def __init__(
        self,
        id: Optional[int],
        email: str,
        username: str,
        password_hash: str,
        full_name: str,
        role: str,
        is_active: bool = True,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.role = role
        self.is_active = is_active
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
    
    def is_patient(self) -> bool:
        """Verifica si el usuario es paciente"""
        return self.role == "patient"
    
    def is_doctor(self) -> bool:
        """Verifica si el usuario es médico"""
        return self.role == "doctor"
    
    def is_admin(self) -> bool:
        """Verifica si el usuario es administrador"""
        return self.role == "admin"
    
    def activate(self):
        """Activar usuario"""
        self.is_active = True
        self.updated_at = datetime.utcnow()
    
    def deactivate(self):
        """Desactivar usuario"""
        self.is_active = False
        self.updated_at = datetime.utcnow()
    
    def __repr__(self):
        return f"<UserEntity(id={self.id}, username={self.username}, role={self.role})>"
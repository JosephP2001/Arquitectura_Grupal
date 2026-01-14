from abc import ABC, abstractmethod
from typing import Optional, List
from src.infrastructure.models.postgresql.models import User

class IUserDAO(ABC):
    """Interface para User DAO"""
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Crear un nuevo usuario"""
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        pass
    
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[User]:
        """Obtener todos los usuarios"""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Actualizar usuario"""
        pass
    
    @abstractmethod
    def delete(self, user_id: int) -> bool:
        """Eliminar usuario"""
        pass
from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.models.postgresql.models import User

class UserDAOPostgreSQL(IUserDAO):
    """Implementación de User DAO para PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        """Crear un nuevo usuario"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtener usuario por ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtener usuario por email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Obtener usuario por username"""
        return self.db.query(User).filter(User.username == username).first()
    
    def get_all(self) -> List[User]:
        """Obtener todos los usuarios"""
        return self.db.query(User).all()
    
    def update(self, user: User) -> User:
        """Actualizar usuario"""
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        """Eliminar usuario"""
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
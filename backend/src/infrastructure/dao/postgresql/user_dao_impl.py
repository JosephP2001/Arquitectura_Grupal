from typing import Optional, List

from sqlalchemy.orm import Session

from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.models.postgresql.models import User
from src.infrastructure.observability.logger import get_logger


logger = get_logger("user_dao")


class UserDAOPostgreSQL(IUserDAO):
    """
    Implementación del DAO de Usuario para PostgreSQL usando SQLAlchemy
    """

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        logger.info(
            "Creating user",
            extra={"extra": {"username": user.username, "email": user.email}},
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(
            "User created",
            extra={"extra": {"user_id": user.id}},
        )

        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        user = (
            self.db
            .query(User)
            .filter(User.id == user_id)
            .first()
        )
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.db
            .query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_username(self, username: str) -> Optional[User]:
        return (
            self.db
            .query(User)
            .filter(User.username == username)
            .first()
        )

    def get_all(self) -> List[User]:
        return self.db.query(User).all()

    def update(self, user: User) -> User:
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False

        self.db.delete(user)
        self.db.commit()
        return True
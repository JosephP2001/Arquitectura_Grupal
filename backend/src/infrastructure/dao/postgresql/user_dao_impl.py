from typing import Optional, List

from sqlalchemy.orm import Session

from src.infrastructure.database.postgres_client import PostgresClient
from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.models.postgresql.models import User
from src.infrastructure.observability.logger import get_logger


logger = get_logger("user_dao")


class UserDAOPostgreSQL(IUserDAO):
    """
    Implementación del DAO de Usuario para PostgreSQL usando SQLAlchemy
    """

    def __init__(self, db: Optional[Session] = None):
        """
        Inicializa el DAO con una sesión de base de datos.
        Si no se inyecta una sesión, se obtiene desde PostgresClient.
        """
        self.db: Session = db or PostgresClient.get_session()

    def create(self, user: User) -> User:
        """
        Crear un nuevo usuario
        """
        logger.info(
            "Creating user",
            extra={
                "extra": {
                    "username": user.username,
                    "email": user.email,
                }
            },
        )

        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        logger.info(
            "User created",
            extra={
                "extra": {
                    "user_id": user.id,
                    "username": user.username,
                }
            },
        )

        return user

    def get_by_id(self, user_id: int) -> Optional[User]:
        """
        Obtener usuario por ID
        """
        logger.info(
            "Fetching user by id",
            extra={"extra": {"user_id": user_id}},
        )

        user = (
            self.db
            .query(User)
            .filter(User.id == user_id)
            .first()
        )

        if not user:
            logger.info(
                "User not found by id",
                extra={"extra": {"user_id": user_id}},
            )

        return user

    def get_by_email(self, email: str) -> Optional[User]:
        """
        Obtener usuario por email
        """
        logger.info(
            "Fetching user by email",
            extra={"extra": {"email": email}},
        )

        user = (
            self.db
            .query(User)
            .filter(User.email == email)
            .first()
        )

        if not user:
            logger.info(
                "User not found by email",
                extra={"extra": {"email": email}},
            )

        return user

    def get_by_username(self, username: str) -> Optional[User]:
        """
        Obtener usuario por username
        """
        logger.info(
            "Fetching user by username",
            extra={"extra": {"username": username}},
        )

        user = (
            self.db
            .query(User)
            .filter(User.username == username)
            .first()
        )

        if not user:
            logger.info(
                "User not found by username",
                extra={"extra": {"username": username}},
            )

        return user

    def get_all(self) -> List[User]:
        """
        Obtener todos los usuarios
        """
        logger.info("Fetching all users")

        users = self.db.query(User).all()

        logger.info(
            "Users fetched",
            extra={"extra": {"count": len(users)}},
        )

        return users

    def update(self, user: User) -> User:
        """
        Actualizar un usuario existente.
        Se asume que el objeto ya está asociado a la sesión.
        """
        logger.info(
            "Updating user",
            extra={
                "extra": {
                    "user_id": user.id,
                    "username": user.username,
                }
            },
        )

        self.db.commit()
        self.db.refresh(user)

        logger.info(
            "User updated",
            extra={"extra": {"user_id": user.id}},
        )

        return user

    def delete(self, user_id: int) -> bool:
        """
        Eliminar un usuario por ID
        """
        logger.info(
            "Deleting user",
            extra={"extra": {"user_id": user_id}},
        )

        user = self.get_by_id(user_id)
        if not user:
            logger.info(
                "User not found for deletion",
                extra={"extra": {"user_id": user_id}},
            )
            return False

        self.db.delete(user)
        self.db.commit()

        logger.info(
            "User deleted",
            extra={"extra": {"user_id": user_id}},
        )

        return True

from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.session.session_repository import SessionRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthenticationService:

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def authenticate(self, username: str, password: str):
        user = self.user_dao.get_by_username(username)
        if not user:
            return None

        if not pwd_context.verify(password, user.password_hash):
            return None

        session_id = SessionRepository.create_session(
            user_id=str(user.id),
            role=user.role.value  # Convertir enum a string
        )

        return {
            "session_id": session_id,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value  # Convertir enum a string
            }
        }
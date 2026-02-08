from typing import Optional, Dict
from passlib.context import CryptContext

from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.models.postgresql.models import User, UserRole, Patient, Doctor
from src.infrastructure.session.session_repository import SessionRepository
from src.infrastructure.observability.logger import get_logger

logger = get_logger("authentication_service")

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationService:
    """
    Servicio de autenticación que maneja login, registro y gestión de usuarios
    """

    def __init__(self, user_dao: IUserDAO):
        self.user_dao = user_dao

    def authenticate(self, username: str, password: str) -> Optional[Dict]:
        """
        Autentica un usuario y crea una sesión
        Retorna dict con session_id y datos del usuario, o None si falla
        """
        logger.info(
            "Authentication attempt",
            extra={"extra": {"username": username}}
        )

        # Buscar usuario por username
        user = self.user_dao.get_by_username(username)
        
        if not user:
            logger.warning(
                "User not found",
                extra={"extra": {"username": username}}
            )
            return None

        # Verificar contraseña
        if not self._verify_password(password, user.password_hash):
            logger.warning(
                "Invalid password",
                extra={"extra": {"username": username}}
            )
            return None

        # Verificar que el usuario esté activo
        if not user.is_active:
            logger.warning(
                "Inactive user",
                extra={"extra": {"username": username}}
            )
            return None

        # Crear sesión en Redis
        session_id = SessionRepository.create_session(
            user_id=str(user.id),
            role=user.role.value
        )

        logger.info(
            "Authentication successful",
            extra={
                "extra": {
                    "user_id": user.id,
                    "username": username,
                    "session_id": session_id
                }
            }
        )

        return {
            "session_id": session_id,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role.value
            }
        }

    def register_user(self, user_data: Dict, db_session) -> Dict:
        """
        Registra un nuevo usuario (paciente o médico)
        """
        logger.info(
            "User registration attempt",
            extra={
                "extra": {
                    "username": user_data.get("username"),
                    "email": user_data.get("email"),
                    "role": user_data.get("role")
                }
            }
        )

        # Verificar si el email ya existe
        existing_user = self.user_dao.get_by_email(user_data["email"])
        if existing_user:
            raise ValueError("El email ya está registrado")

        # Verificar si el username ya existe
        existing_user = self.user_dao.get_by_username(user_data["username"])
        if existing_user:
            raise ValueError("El nombre de usuario ya está en uso")

        # Hashear contraseña
        password_hash = self._hash_password(user_data["password"])

        # Crear usuario
        user = User(
            email=user_data["email"],
            username=user_data["username"],
            password_hash=password_hash,
            full_name=user_data["full_name"],
            role=UserRole(user_data["role"]),
            is_active=True
        )

        # Guardar usuario
        created_user = self.user_dao.create(user)

        # Crear perfil según el rol
        if user_data["role"] == "patient":
            patient = Patient(
                user_id=created_user.id,
                phone=user_data.get("phone"),
                address=user_data.get("address")
            )
            db_session.add(patient)
            db_session.commit()
            
        elif user_data["role"] == "doctor":
            doctor = Doctor(
                user_id=created_user.id,
                specialty_id=user_data["specialty_id"],
                license_number=user_data["license_number"],
                phone=user_data.get("phone")
            )
            db_session.add(doctor)
            db_session.commit()

        logger.info(
            "User registered successfully",
            extra={
                "extra": {
                    "user_id": created_user.id,
                    "username": created_user.username,
                    "role": created_user.role.value
                }
            }
        )

        # Crear sesión automáticamente
        session_id = SessionRepository.create_session(
            user_id=str(created_user.id),
            role=created_user.role.value
        )

        return {
            "session_id": session_id,
            "user": {
                "id": created_user.id,
                "username": created_user.username,
                "email": created_user.email,
                "full_name": created_user.full_name,
                "role": created_user.role.value
            }
        }

    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash de contraseña usando bcrypt"""
        return pwd_context.hash(password)

    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verificar contraseña"""
        return pwd_context.verify(plain_password, hashed_password)
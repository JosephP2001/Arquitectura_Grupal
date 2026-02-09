import uuid
from typing import Optional, Dict
from pybreaker import CircuitBreaker

from src.infrastructure.cache.redis_client import get_redis_client
from src.infrastructure.observability.logger import get_logger


logger = get_logger("session_repository")

# Tiempo de vida de la sesión en segundos (1 hora)
SESSION_TTL = 60 * 60

# Circuit breaker: falla 3 veces, resetea a los 20 segundos
redis_breaker = CircuitBreaker(fail_max=3, reset_timeout=20)


class SessionRepository:
    """
    Repositorio de sesiones usando Redis
    Protegido con Circuit Breaker para resiliencia.
    """

    @staticmethod
    @redis_breaker
    def create_session(user_id: str, role: str) -> str:
        """
        Crea una nueva sesión en Redis
        """
        try:
            redis_client = get_redis_client()
            session_id = str(uuid.uuid4())

            redis_client.hset(
                f"session:{session_id}",
                mapping={
                    "user_id": user_id,
                    "role": role,
                },
            )

            redis_client.expire(f"session:{session_id}", SESSION_TTL)

            logger.info(
                "Session created",
                extra={
                    "extra": {
                        "session_id": session_id,
                        "user_id": user_id,
                        "role": role,
                        "ttl": SESSION_TTL,
                    }
                },
            )

            return session_id

        except Exception:
            logger.error(
                "Redis unavailable while creating session",
                extra={"extra": {"user_id": user_id}},
            )
            raise

    @staticmethod
    @redis_breaker
    def get_session(session_id: str) -> Optional[Dict[str, str]]:
        """
        Obtiene datos de sesión desde Redis
        Retorna None si no existe
        """
        try:
            redis_client = get_redis_client()
            data = redis_client.hgetall(f"session:{session_id}")

            if data:
                logger.info(
                    "Session retrieved",
                    extra={
                        "extra": {
                            "session_id": session_id,
                            "user_id": data.get("user_id"),
                        }
                    },
                )
                return data

            logger.info(
                "Session not found",
                extra={"extra": {"session_id": session_id}},
            )
            return None

        except Exception:
            logger.error(
                "Redis unavailable while retrieving session",
                extra={"extra": {"session_id": session_id}},
            )
            raise

    @staticmethod
    @redis_breaker
    def delete_session(session_id: str) -> None:
        """
        Elimina la sesión de Redis
        """
        try:
            redis_client = get_redis_client()
            redis_client.delete(f"session:{session_id}")

            logger.info(
                "Session deleted",
                extra={"extra": {"session_id": session_id}},
            )

        except Exception:
            logger.error(
                "Redis unavailable while deleting session",
                extra={"extra": {"session_id": session_id}},
            )
            raise
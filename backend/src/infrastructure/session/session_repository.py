import uuid
import json
from typing import Optional, Dict

from src.infrastructure.resilience.circuit_breaker import CircuitBreaker
from src.infrastructure.cache.redis_client import get_redis_client

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
        redis_client = get_redis_client()
        session_id = str(uuid.uuid4())

        # Guardar datos de sesión como hash
        redis_client.hset(
            f"session:{session_id}",
            mapping={
                "user_id": user_id,
                "role": role
            }
        )

        # Expiración automática
        redis_client.expire(f"session:{session_id}", SESSION_TTL)
        return session_id

    @staticmethod
    @redis_breaker
    def get_session(session_id: str) -> Optional[Dict[str, str]]:
        """
        Obtiene datos de sesión desde Redis
        Retorna None si no existe
        """
        redis_client = get_redis_client()
        data = redis_client.hgetall(f"session:{session_id}")
        return data if data else None

    @staticmethod
    @redis_breaker
    def delete_session(session_id: str) -> None:
        """
        Elimina la sesión de Redis
        """
        redis_client = get_redis_client()
        redis_client.delete(f"session:{session_id}")

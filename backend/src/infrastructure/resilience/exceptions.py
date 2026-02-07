import uuid

from streamlit import json
from backend.src.infrastructure.cache import redis_client
from src.infrastructure.resilience.circuit_breaker import CircuitBreaker

redis_breaker = CircuitBreaker(fail_max=3, reset_timeout=20)

class SessionRepository:

    @staticmethod
    @redis_breaker
    def create_session(user_id: str, role: str) -> str:
        session_id = str(uuid.uuid4())
        redis_client.setex(
            f"session:{session_id}",
            3600,
            json.dumps({"user_id": user_id, "role": role})
        )
        return session_id

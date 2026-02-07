from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from src.config.database import SessionLocal
from src.infrastructure.resilience.circuit_breaker import CircuitBreaker

postgres_breaker = CircuitBreaker(fail_max=3, reset_timeout=30)


class PostgresClient:
    """
    Wrapper seguro para PostgreSQL
    """

    @staticmethod
    @postgres_breaker
    def get_session() -> Session:
        try:
            return SessionLocal()
        except SQLAlchemyError:
            raise

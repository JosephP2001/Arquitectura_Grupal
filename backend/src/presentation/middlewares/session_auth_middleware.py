from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from pybreaker import CircuitBreakerError

from src.config.database import get_db
from src.infrastructure.session.session_repository import SessionRepository
from src.infrastructure.models.postgresql.models import User


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario autenticado a partir de la cookie SESSION_ID.

    - Redis protegido con Circuit Breaker
    - PostgreSQL sin breaker en este nivel
    """

    # Leer cookie de sesión
    session_id = request.cookies.get("SESSION_ID")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )

    # Obtener sesión desde Redis (Circuit Breaker)
    try:
        session_data = SessionRepository.get_session(session_id)
    except CircuitBreakerError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de sesiones no disponible temporalmente"
        )

    # Validar sesión
    if not session_data or "user_id" not in session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada"
        )

    # Obtener usuario desde PostgreSQL
    user = (
        db
        .query(User)
        .filter(User.id == session_data["user_id"])
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user
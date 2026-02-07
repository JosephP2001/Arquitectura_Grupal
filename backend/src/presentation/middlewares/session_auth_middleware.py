from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.config.database import get_db
from src.infrastructure.session.session_repository import SessionRepository
from src.infrastructure.models.postgresql.models import User
from src.infrastructure.resilience.circuit_breaker import CircuitBreakerOpen


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
) -> User:
    """
    Obtiene el usuario actual basado en la cookie 'SESSION_ID'
    Protegido con Circuit Breaker para Redis
    """

    # Leer cookie
    session_id = request.cookies.get("SESSION_ID")
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )

    # Intentar obtener la sesión desde Redis
    try:
        session_data = SessionRepository.get_session(session_id)
    except CircuitBreakerOpen:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Servicio de sesiones no disponible"
        )

    # Si no hay sesión válida
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión inválida o expirada"
        )

    # Buscar el usuario en la base de datos
    user = db.query(User).filter(User.id == session_data["user_id"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return user

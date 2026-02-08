from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.infrastructure.dao.postgresql.user_dao_impl import UserDAO
from src.config.database import get_db
from src.infrastructure.observability.logger import get_logger
from src.domain.services.authentication_service import AuthenticationService

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

logger = get_logger("auth_routes")


def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    user_dao = UserDAO(db)
    return AuthenticationService(user_dao)


@router.post("/login")
def login(
    username: str,
    password: str,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    result = auth_service.authenticate(username, password)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    return result


@router.post("/register")
def register(
    user_data: dict,
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    try:
        return auth_service.register_user(user_data, db)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

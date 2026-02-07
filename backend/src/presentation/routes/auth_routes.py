from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session

from src.application.dto.login_request_dto import LoginRequestDTO
from src.domain.services.authentication_service import AuthenticationService
from src.infrastructure.dao.abstract_factory import PostgreSQLDAOFactory
from src.config.database import get_db

router = APIRouter()


# Inyección de dependencia: crea AuthenticationService con el DAO
def get_auth_service(db: Session = Depends(get_db)) -> AuthenticationService:
    factory = PostgreSQLDAOFactory(db)
    user_dao = factory.create_user_dao()
    return AuthenticationService(user_dao)


@router.post("/login")
def login(
    data: LoginRequestDTO,
    response: Response,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Endpoint de login:
    - Valida credenciales
    - Crea cookie de sesión
    - Retorna mensaje y session_id
    """
    # Ejecuta la lógica de autenticación
    result = auth_service.authenticate(data.username, data.password)

    # Si las credenciales son inválidas
    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Crea cookie de sesión segura
    response.set_cookie(
        key="SESSION_ID",
        value=result["session_id"],
        httponly=True,
        secure=False,  # Cambiar a True en producción con HTTPS
        samesite="lax"
    )

    # Retorna mensaje y opcionalmente session_id (útil para debug)
    return {"message": "Login exitoso", "session_id": result["session_id"]}


@router.post("/logout")
def logout(response: Response):
    """
    Endpoint para cerrar sesión:
    - Borra la cookie de sesión
    """
    response.delete_cookie("SESSION_ID")
    return {"message": "Logout exitoso"}

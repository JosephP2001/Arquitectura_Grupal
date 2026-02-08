from fastapi import APIRouter, Depends, Response, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.application.dto.login_request_dto import LoginRequestDTO
from src.domain.services.authentication_service import AuthenticationService
from src.infrastructure.dao.abstract_factory import PostgreSQLDAOFactory
from src.infrastructure.session.session_repository import SessionRepository
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
def logout(request: Request, response: Response):
    """
    Endpoint para cerrar sesión:
    - Elimina la sesión de Redis
    - Borra la cookie de sesión
    """
    # Obtener session_id de la cookie
    session_id = request.cookies.get("SESSION_ID")
    
    # Si existe sesión, eliminarla de Redis
    if session_id:
        try:
            SessionRepository.delete_session(session_id)
        except Exception as e:
            # Log del error pero continuar con el logout
            print(f"Error al eliminar sesión de Redis: {e}")
    
    # Borrar cookie
    response.delete_cookie("SESSION_ID")
    
    return {"message": "Logout exitoso"}
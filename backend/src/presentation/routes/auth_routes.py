from fastapi import APIRouter, Depends, Response, HTTPException, Request, status
from sqlalchemy.orm import Session

from src.application.dto.login_request_dto import LoginRequestDTO
from src.application.dto.user_dto import UserCreateDTO
from src.domain.services.authentication_service import AuthenticationService
from src.infrastructure.dao.abstract_factory import PostgreSQLDAOFactory
from src.infrastructure.session.session_repository import SessionRepository
from src.infrastructure.models.postgresql.models import User
from src.presentation.middlewares.session_auth_middleware import get_current_user
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
    - Retorna mensaje, session_id y datos del usuario
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
    # CONFIGURACIÓN PARA DESARROLLO LOCAL
    response.set_cookie(
        key="SESSION_ID",
        value=result["session_id"],
        httponly=False,  # Debe ser False para desarrollo local
        secure=False,  # HTTP local
        samesite="lax",  # Funciona en localhost
        max_age=3600,  # 1 hora
        path="/"  # Importante: disponible en todas las rutas
    )

    # Retorna mensaje, session_id y datos del usuario
    return {
        "message": "Login exitoso",
        "session_id": result["session_id"],
        "user": result["user"]  # Incluye datos del usuario
    }


@router.post("/register")
def register(
    user_data: UserCreateDTO,
    response: Response,
    db: Session = Depends(get_db),
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    """
    Endpoint de registro:
    - Crea nuevo usuario (paciente o médico)
    - Crea perfil correspondiente
    - Crea sesión automáticamente
    - Retorna session_id y datos del usuario
    """
    try:
        # Convertir DTO a dict
        user_dict = user_data.model_dump()
        
        # Registrar usuario
        result = auth_service.register_user(user_dict, db)
        
        # Crear cookie de sesión
        response.set_cookie(
            key="SESSION_ID",
            value=result["session_id"],
            httponly=False,  # Debe ser False para desarrollo local
            secure=False,
            samesite="lax",  # Funciona en localhost
            max_age=3600,
            path="/"
        )
        
        return {
            "message": "Registro exitoso",
            "session_id": result["session_id"],
            "user": result["user"]
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al registrar usuario: {str(e)}"
        )


@router.get("/me")
def get_current_user_info(request: Request, db: Session = Depends(get_db)):
    """
    Obtiene información del usuario autenticado actual.
    Retorna null si no hay sesión (en lugar de error 401).
    """
    try:
        # Intentar obtener sesión
        session_id = request.cookies.get("SESSION_ID")
        if not session_id:
            return None
        
        # Obtener datos de sesión desde Redis
        session_data = SessionRepository.get_session(session_id)
        if not session_data or "user_id" not in session_data:
            return None
        
        # Obtener usuario desde PostgreSQL
        user = db.query(User).filter(User.id == session_data["user_id"]).first()
        
        if not user:
            return None
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.value
        }
    except Exception:
        # Si hay cualquier error, retornar null silenciosamente
        return None


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
    
    # Borrar cookie con los mismos parámetros
    response.delete_cookie(
        key="SESSION_ID",
        path="/",
        samesite="lax"
    )
    
    return {"message": "Logout exitoso"}
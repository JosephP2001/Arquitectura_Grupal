from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from src.config.database import get_db
from src.infrastructure.models.postgresql.models import User, UserRole

def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Obtener usuario actual desde user_id en header"""
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No autenticado"
        )
    
    try:
        # Formato: "Bearer user_id"
        user_id = int(authorization.replace("Bearer ", ""))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    return user

def require_role(*allowed_roles: UserRole):
    """Decorator para requerir roles específicos"""
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Se requiere uno de los siguientes roles: {', '.join(r.value for r in allowed_roles)}"
            )
        return current_user
    return role_checker
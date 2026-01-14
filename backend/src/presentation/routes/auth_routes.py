from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.config.database import get_db
from src.infrastructure.models.postgresql.models import User, Patient, Doctor, UserRole
from src.utils.jwt_handler import create_access_token
from pydantic import BaseModel, EmailStr

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class RegisterRequest(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: str
    role: UserRole
    phone: str = None
    license_number: str = None
    specialty_id: int = None

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario"""
    # Verificar si el usuario ya existe
    if db.query(User).filter(User.email == request.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    if db.query(User).filter(User.username == request.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El username ya está en uso"
        )
    
    # Crear usuario
    hashed_password = pwd_context.hash(request.password)
    user = User(
        email=request.email,
        username=request.username,
        password_hash=hashed_password,
        full_name=request.full_name,
        role=request.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Crear perfil según el rol
    if request.role == UserRole.PATIENT:
        patient = Patient(user_id=user.id, phone=request.phone)
        db.add(patient)
    elif request.role == UserRole.DOCTOR:
        if not request.license_number or not request.specialty_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Licencia y especialidad requeridas para médicos"
            )
        doctor = Doctor(
            user_id=user.id,
            license_number=request.license_number,
            specialty_id=request.specialty_id,
            phone=request.phone
        )
        db.add(doctor)
    
    db.commit()
    
    # Crear token
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value
        }
    }

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    """Iniciar sesión"""
    user = db.query(User).filter(User.username == request.username).first()
    
    if not user or not pwd_context.verify(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    access_token = create_access_token(data={"sub": user.id, "role": user.role.value})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
            "role": user.role.value
        }
    }
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db, get_mongodb
from src.infrastructure.models.postgresql.models import Patient, User, UserRole
from src.presentation.middlewares.auth_middleware import get_current_user
from src.infrastructure.dao.mongodb.medical_record_dao_impl import MedicalRecordDAOMongo
from pydantic import BaseModel
from typing import List

router = APIRouter()

class PatientResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: str = None
    address: str = None
    
    class Config:
        from_attributes = True

@router.get("/me", response_model=PatientResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener perfil del paciente actual"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo pacientes pueden acceder a este endpoint"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de paciente no encontrado"
        )
    
    return PatientResponse(
        id=patient.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=patient.phone,
        address=patient.address
    )

@router.get("/medical-records")
def get_medical_records(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener historial médico del paciente"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo pacientes pueden acceder a su historial"
        )
    
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de paciente no encontrado"
        )
    
    # Obtener registros médicos de MongoDB
    mongodb = get_mongodb()
    medical_record_dao = MedicalRecordDAOMongo(mongodb)
    records = medical_record_dao.get_by_patient(patient.id)
    
    return {"records": records}
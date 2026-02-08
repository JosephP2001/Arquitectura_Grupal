from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.config.database import get_db, get_mongodb
from src.infrastructure.models.postgresql.models import Patient, User, UserRole, Appointment, AppointmentStatus
from src.presentation.middlewares.session_auth_middleware import get_current_user
from src.infrastructure.dao.mongodb.medical_record_dao_impl import MedicalRecordDAOMongo
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PatientResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    address: Optional[str] = None
    total_appointments: int
    pending_appointments: int
    confirmed_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    medical_records_count: int
    
    class Config:
        from_attributes = True

@router.get("/me", response_model=PatientResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener perfil del paciente actual con estadísticas"""
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
    
    # Estadísticas de citas
    total_appointments = db.query(Appointment).filter(Appointment.patient_id == patient.id).count()
    pending = db.query(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.status == AppointmentStatus.PENDING
    ).count()
    confirmed = db.query(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.status == AppointmentStatus.CONFIRMED
    ).count()
    completed = db.query(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.status == AppointmentStatus.COMPLETED
    ).count()
    cancelled = db.query(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.status == AppointmentStatus.CANCELLED
    ).count()
    
    # Registros médicos de MongoDB
    try:
        mongodb = get_mongodb()
        medical_record_dao = MedicalRecordDAOMongo(mongodb)
        records = medical_record_dao.get_by_patient(patient.id)
        medical_records_count = len(records)
    except:
        medical_records_count = 0
    
    return PatientResponse(
        id=patient.id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=patient.phone,
        address=patient.address,
        total_appointments=total_appointments,
        pending_appointments=pending,
        confirmed_appointments=confirmed,
        completed_appointments=completed,
        cancelled_appointments=cancelled,
        medical_records_count=medical_records_count
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
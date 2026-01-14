from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from src.config.database import get_db
from src.infrastructure.models.postgresql.models import (
    Appointment, User, Patient, Doctor, AppointmentStatus, UserRole
)
from src.presentation.middlewares.auth_middleware import get_current_user
from pydantic import BaseModel

router = APIRouter()

class AppointmentCreate(BaseModel):
    doctor_id: int
    appointment_date: datetime
    reason: str
    duration_minutes: int = 30

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_date: datetime
    duration_minutes: int
    status: str
    reason: str
    notes: str = None
    patient_name: str
    doctor_name: str
    
    class Config:
        from_attributes = True

@router.post("/", response_model=AppointmentResponse)
def create_appointment(
    request: AppointmentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crear una nueva cita (solo pacientes)"""
    if current_user.role != UserRole.PATIENT:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Solo los pacientes pueden agendar citas"
        )
    
    # Obtener perfil de paciente
    patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil de paciente no encontrado"
        )
    
    # Verificar que el médico existe
    doctor = db.query(Doctor).filter(Doctor.id == request.doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico no encontrado"
        )
    
    # Verificar disponibilidad (no hay otra cita en ese horario)
    existing = db.query(Appointment).filter(
        Appointment.doctor_id == request.doctor_id,
        Appointment.appointment_date == request.appointment_date,
        Appointment.status.in_([AppointmentStatus.PENDING, AppointmentStatus.CONFIRMED])
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El médico no está disponible en ese horario"
        )
    
    # Crear cita
    appointment = Appointment(
        patient_id=patient.id,
        doctor_id=request.doctor_id,
        appointment_date=request.appointment_date,
        duration_minutes=request.duration_minutes,
        reason=request.reason,
        status=AppointmentStatus.PENDING
    )
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    
    return AppointmentResponse(
        id=appointment.id,
        patient_id=appointment.patient_id,
        doctor_id=appointment.doctor_id,
        appointment_date=appointment.appointment_date,
        duration_minutes=appointment.duration_minutes,
        status=appointment.status.value,
        reason=appointment.reason,
        notes=appointment.notes,
        patient_name=current_user.full_name,
        doctor_name=doctor.user.full_name
    )

@router.get("/my-appointments", response_model=List[AppointmentResponse])
def get_my_appointments(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Obtener mis citas"""
    if current_user.role == UserRole.PATIENT:
        patient = db.query(Patient).filter(Patient.user_id == current_user.id).first()
        appointments = db.query(Appointment).filter(
            Appointment.patient_id == patient.id
        ).order_by(Appointment.appointment_date.desc()).all()
    elif current_user.role == UserRole.DOCTOR:
        doctor = db.query(Doctor).filter(Doctor.user_id == current_user.id).first()
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id
        ).order_by(Appointment.appointment_date.desc()).all()
    else:
        appointments = db.query(Appointment).order_by(
            Appointment.appointment_date.desc()
        ).all()
    
    return [
        AppointmentResponse(
            id=apt.id,
            patient_id=apt.patient_id,
            doctor_id=apt.doctor_id,
            appointment_date=apt.appointment_date,
            duration_minutes=apt.duration_minutes,
            status=apt.status.value,
            reason=apt.reason,
            notes=apt.notes,
            patient_name=apt.patient.user.full_name,
            doctor_name=apt.doctor.user.full_name
        )
        for apt in appointments
    ]

@router.patch("/{appointment_id}/status")
def update_appointment_status(
    appointment_id: int,
    status: AppointmentStatus,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Actualizar estado de una cita"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cita no encontrada"
        )
    
    appointment.status = status
    db.commit()
    
    return {"message": "Estado actualizado exitosamente"}
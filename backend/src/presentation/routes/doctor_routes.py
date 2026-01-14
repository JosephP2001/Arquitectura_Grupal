from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.config.database import get_db
from src.infrastructure.models.postgresql.models import Doctor, Specialty, Schedule
from pydantic import BaseModel

router = APIRouter()

class DoctorResponse(BaseModel):
    id: int
    full_name: str
    email: str
    specialty: str
    license_number: str
    phone: str = None
    
    class Config:
        from_attributes = True

class ScheduleResponse(BaseModel):
    id: int
    day_of_week: int
    start_time: str
    end_time: str
    is_active: bool
    
    class Config:
        from_attributes = True

@router.get("/", response_model=List[DoctorResponse])
def get_doctors(
    specialty_id: int = None,
    db: Session = Depends(get_db)
):
    """Obtener lista de médicos"""
    query = db.query(Doctor)
    
    if specialty_id:
        query = query.filter(Doctor.specialty_id == specialty_id)
    
    doctors = query.all()
    
    return [
        DoctorResponse(
            id=doc.id,
            full_name=doc.user.full_name,
            email=doc.user.email,
            specialty=doc.specialty.name,
            license_number=doc.license_number,
            phone=doc.phone
        )
        for doc in doctors
    ]

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    """Obtener información de un médico específico"""
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico no encontrado"
        )
    
    return DoctorResponse(
        id=doctor.id,
        full_name=doctor.user.full_name,
        email=doctor.user.email,
        specialty=doctor.specialty.name,
        license_number=doctor.license_number,
        phone=doctor.phone
    )

@router.get("/{doctor_id}/schedule", response_model=List[ScheduleResponse])
def get_doctor_schedule(doctor_id: int, db: Session = Depends(get_db)):
    """Obtener horarios de un médico"""
    schedules = db.query(Schedule).filter(
        Schedule.doctor_id == doctor_id,
        Schedule.is_active == True
    ).all()
    
    return [
        ScheduleResponse(
            id=sched.id,
            day_of_week=sched.day_of_week,
            start_time=str(sched.start_time),
            end_time=str(sched.end_time),
            is_active=sched.is_active
        )
        for sched in schedules
    ]

@router.get("/specialties/list")
def get_specialties(db: Session = Depends(get_db)):
    """Obtener lista de especialidades"""
    specialties = db.query(Specialty).all()
    return [
        {"id": spec.id, "name": spec.name, "description": spec.description}
        for spec in specialties
    ]
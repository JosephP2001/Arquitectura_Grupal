from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.config.database import get_db, get_mongodb
from src.infrastructure.models.postgresql.models import Appointment, Patient, Doctor, User
from src.infrastructure.dao.mongodb.medical_record_dao_impl import MedicalRecordDAOMongo
from src.presentation.middlewares.session_auth_middleware import get_current_user
from typing import List
from pydantic import BaseModel

router = APIRouter()

class PatientCompleteReport(BaseModel):
    """Reporte completo del paciente combinando PostgreSQL y MongoDB"""
    patient_id: int
    patient_name: str
    email: str
    phone: str
    total_appointments: int
    appointments: List[dict]
    medical_records_count: int
    medical_records: List[dict]

class SystemReport(BaseModel):
    """Reporte general del sistema"""
    total_patients: int
    total_doctors: int
    total_appointments: int
    appointments_by_status: dict
    total_medical_records: int
    recent_activity: List[dict]

@router.get("/patient/{patient_id}", response_model=PatientCompleteReport)
def get_patient_complete_report(
    patient_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reporte completo de un paciente combinando datos de PostgreSQL y MongoDB
    - Datos del paciente (PostgreSQL)
    - Historial de citas (PostgreSQL)
    - Historiales médicos (MongoDB)
    """
    # Obtener datos del paciente desde PostgreSQL
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado"
        )
    
    # Obtener citas del paciente
    appointments = db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).order_by(Appointment.appointment_date.desc()).all()
    
    appointments_data = [
        {
            "id": apt.id,
            "doctor_name": apt.doctor.user.full_name,
            "specialty": apt.doctor.specialty.name,
            "date": apt.appointment_date.isoformat(),
            "status": apt.status.value,
            "reason": apt.reason
        }
        for apt in appointments
    ]
    
    # Obtener historiales médicos desde MongoDB
    mongodb = get_mongodb()
    medical_record_dao = MedicalRecordDAOMongo(mongodb)
    medical_records = medical_record_dao.get_by_patient(patient_id)
    
    # Convertir ObjectId a string para serialización
    for record in medical_records:
        record['_id'] = str(record['_id'])
        if 'created_at' in record:
            record['created_at'] = record['created_at'].isoformat()
    
    return PatientCompleteReport(
        patient_id=patient.id,
        patient_name=patient.user.full_name,
        email=patient.user.email,
        phone=patient.phone or "N/A",
        total_appointments=len(appointments),
        appointments=appointments_data,
        medical_records_count=len(medical_records),
        medical_records=medical_records
    )

@router.get("/system", response_model=SystemReport)
def get_system_report(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reporte general del sistema combinando PostgreSQL y MongoDB
    - Estadísticas de usuarios (PostgreSQL)
    - Estadísticas de citas (PostgreSQL)
    - Total de registros médicos (MongoDB)
    - Actividad reciente del sistema (MongoDB)
    """
    from src.infrastructure.models.postgresql.models import AppointmentStatus
    from src.infrastructure.dao.mongodb.log_dao_impl import LogDAOMongo
    
    # Datos desde PostgreSQL
    total_patients = db.query(Patient).count()
    total_doctors = db.query(Doctor).count()
    total_appointments = db.query(Appointment).count()
    
    # Contar citas por estado
    appointments_by_status = {}
    for status in AppointmentStatus:
        count = db.query(Appointment).filter(
            Appointment.status == status
        ).count()
        appointments_by_status[status.value] = count
    
    # Datos desde MongoDB
    mongodb = get_mongodb()
    total_medical_records = mongodb.medical_records.count_documents({})
    
    # Obtener actividad reciente de logs
    log_dao = LogDAOMongo(mongodb)
    recent_logs = log_dao.get_recent(hours=24, limit=10)
    
    # Convertir ObjectId y datetime a string
    for log in recent_logs:
        log['_id'] = str(log['_id'])
        if 'timestamp' in log:
            log['timestamp'] = log['timestamp'].isoformat()
    
    return SystemReport(
        total_patients=total_patients,
        total_doctors=total_doctors,
        total_appointments=total_appointments,
        appointments_by_status=appointments_by_status,
        total_medical_records=total_medical_records,
        recent_activity=recent_logs
    )

@router.get("/doctor/{doctor_id}/performance")
def get_doctor_performance_report(
    doctor_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Reporte de desempeño del médico combinando PostgreSQL y MongoDB
    - Citas atendidas (PostgreSQL)
    - Registros médicos creados (MongoDB)
    """
    # Datos del médico
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Médico no encontrado"
        )
    
    # Estadísticas de citas
    from src.infrastructure.models.postgresql.models import AppointmentStatus
    total_appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).count()
    
    completed_appointments = db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.status == AppointmentStatus.COMPLETED
    ).count()
    
    # Registros médicos creados por este doctor
    mongodb = get_mongodb()
    medical_records_count = mongodb.medical_records.count_documents({
        "doctor_id": doctor_id
    })
    
    # Obtener algunos registros médicos recientes
    recent_records = list(mongodb.medical_records.find(
        {"doctor_id": doctor_id}
    ).sort("created_at", -1).limit(5))
    
    for record in recent_records:
        record['_id'] = str(record['_id'])
        if 'created_at' in record:
            record['created_at'] = record['created_at'].isoformat()
    
    return {
        "doctor_id": doctor.id,
        "doctor_name": doctor.user.full_name,
        "specialty": doctor.specialty.name,
        "total_appointments": total_appointments,
        "completed_appointments": completed_appointments,
        "completion_rate": f"{(completed_appointments/total_appointments*100):.2f}%" if total_appointments > 0 else "0%",
        "medical_records_created": medical_records_count,
        "recent_medical_records": recent_records
    }
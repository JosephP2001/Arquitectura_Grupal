import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.database import get_session_local, get_mongodb
from src.infrastructure.models.postgresql.models import (
    User, Patient, Doctor, Specialty, UserRole, Schedule
)
from passlib.context import CryptContext
from datetime import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_data():
    db = get_session_local()()
    
    try:
        # Crear especialidades
        if db.query(Specialty).count() == 0:
            specialties = [
                Specialty(name="Cardiología", description="Especialidad del corazón"),
                Specialty(name="Pediatría", description="Especialidad infantil"),
                Specialty(name="Medicina General", description="Atención general")
            ]
            db.add_all(specialties)
            db.commit()
            print("✅ Especialidades creadas")
        
        # Crear admin
        if not db.query(User).filter(User.username == "admin").first():
            admin = User(
                email="admin@test.com",
                username="admin",
                password_hash=pwd_context.hash("admin123"),
                full_name="Administrador Sistema",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("✅ Admin creado")
        
        # Crear pacientes
        if not db.query(User).filter(User.username == "paciente1").first():
            patient_user = User(
                email="paciente1@test.com",
                username="paciente1",
                password_hash=pwd_context.hash("pass123"),
                full_name="Juan Pérez",
                role=UserRole.PATIENT,
                is_active=True
            )
            db.add(patient_user)
            db.commit()
            
            patient = Patient(
                user_id=patient_user.id,
                phone="0999999999",
                address="Quito, Ecuador"
            )
            db.add(patient)
            db.commit()
            print("✅ Paciente creado")
        
        # Crear doctores
        cardio_specialty = db.query(Specialty).filter(Specialty.name == "Cardiología").first()
        if cardio_specialty and not db.query(User).filter(User.username == "doctor1").first():
            doctor_user = User(
                email="doctor1@test.com",
                username="doctor1",
                password_hash=pwd_context.hash("doc123"),
                full_name="Dr. María González",
                role=UserRole.DOCTOR,
                is_active=True
            )
            db.add(doctor_user)
            db.commit()
            
            doctor = Doctor(
                user_id=doctor_user.id,
                specialty_id=cardio_specialty.id,
                license_number="MED-001",
                phone="0988888888"
            )
            db.add(doctor)
            db.commit()
            
            # Horarios
            schedules = [
                Schedule(doctor_id=doctor.id, day_of_week=0, start_time=time(8, 0), end_time=time(17, 0), is_active=True),
                Schedule(doctor_id=doctor.id, day_of_week=1, start_time=time(8, 0), end_time=time(17, 0), is_active=True),
                Schedule(doctor_id=doctor.id, day_of_week=2, start_time=time(8, 0), end_time=time(17, 0), is_active=True),
            ]
            db.add_all(schedules)
            db.commit()
            print("✅ Doctor creado")
        
        print("\n🎉 Datos de prueba inicializados")
        
    finally:
        db.close()

if __name__ == "__main__":
    init_data()
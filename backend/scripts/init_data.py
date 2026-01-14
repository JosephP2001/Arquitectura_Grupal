import sys
import os

# Agregar el directorio padre al path para poder importar src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from src.config.database import SessionLocal
from src.infrastructure.models.postgresql.models import (
    User, Patient, Doctor, Specialty, Schedule, UserRole
)
from datetime import time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def init_specialties(db: Session):
    """Crear especialidades médicas"""
    specialties = [
        {"name": "Cardiología", "description": "Especialidad del corazón y sistema circulatorio"},
        {"name": "Dermatología", "description": "Especialidad de la piel"},
        {"name": "Pediatría", "description": "Especialidad de medicina infantil"},
        {"name": "Neurología", "description": "Especialidad del sistema nervioso"},
        {"name": "Traumatología", "description": "Especialidad de huesos y articulaciones"},
        {"name": "Ginecología", "description": "Especialidad de la salud femenina"},
        {"name": "Oftalmología", "description": "Especialidad de los ojos"},
        {"name": "Psiquiatría", "description": "Especialidad de salud mental"},
    ]
    
    for spec_data in specialties:
        existing = db.query(Specialty).filter(Specialty.name == spec_data["name"]).first()
        if not existing:
            specialty = Specialty(**spec_data)
            db.add(specialty)
    
    db.commit()
    print(" Especialidades creadas")

def init_test_users(db: Session):
    """Crear usuarios de prueba"""
    
    # Crear paciente de prueba
    if not db.query(User).filter(User.email == "paciente@test.com").first():
        user_patient = User(
            email="paciente@test.com",
            username="paciente1",
            password_hash=pwd_context.hash("password123"),
            full_name="Juan Pérez",
            role=UserRole.PATIENT,
            is_active=True
        )
        db.add(user_patient)
        db.commit()
        
        patient = Patient(
            user_id=user_patient.id,
            phone="0987654321",
            address="Quito, Ecuador"
        )
        db.add(patient)
        db.commit()
        print(" Paciente de prueba creado: paciente1 / password123")
    
    # Crear médicos de prueba
    specialties = db.query(Specialty).all()
    
    doctors_data = [
        {
            "email": "doctor1@test.com",
            "username": "doctor1",
            "full_name": "Dra. María González",
            "specialty": "Cardiología",
            "license": "MD-001"
        },
        {
            "email": "doctor2@test.com",
            "username": "doctor2",
            "full_name": "Dr. Carlos Rodríguez",
            "specialty": "Pediatría",
            "license": "MD-002"
        },
        {
            "email": "doctor3@test.com",
            "username": "doctor3",
            "full_name": "Dra. Ana Martínez",
            "specialty": "Dermatología",
            "license": "MD-003"
        }
    ]
    
    for doc_data in doctors_data:
        if not db.query(User).filter(User.email == doc_data["email"]).first():
            specialty = db.query(Specialty).filter(Specialty.name == doc_data["specialty"]).first()
            if not specialty:
                continue
            
            user_doctor = User(
                email=doc_data["email"],
                username=doc_data["username"],
                password_hash=pwd_context.hash("password123"),
                full_name=doc_data["full_name"],
                role=UserRole.DOCTOR,
                is_active=True
            )
            db.add(user_doctor)
            db.commit()
            
            doctor = Doctor(
                user_id=user_doctor.id,
                specialty_id=specialty.id,
                license_number=doc_data["license"],
                phone="0987654322"
            )
            db.add(doctor)
            db.commit()
            
            # Crear horarios de ejemplo (Lunes a Viernes, 9:00 AM - 5:00 PM)
            for day in range(5):  # 0=Lunes, 4=Viernes
                schedule = Schedule(
                    doctor_id=doctor.id,
                    day_of_week=day,
                    start_time=time(9, 0),
                    end_time=time(17, 0),
                    is_active=True
                )
                db.add(schedule)
            
            db.commit()
            print(f" Médico de prueba creado: {doc_data['username']} / password123")
    
    # Crear admin de prueba
    if not db.query(User).filter(User.email == "admin@test.com").first():
        user_admin = User(
            email="admin@test.com",
            username="admin",
            password_hash=pwd_context.hash("admin123"),
            full_name="Administrador Sistema",
            role=UserRole.ADMIN,
            is_active=True
        )
        db.add(user_admin)
        db.commit()
        print(" Administrador creado: admin / admin123")

def main():
    """Función principal"""
    print("🔄 Inicializando datos de prueba...")
    db = SessionLocal()
    
    try:
        init_specialties(db)
        init_test_users(db)
        print("\n Inicialización completada exitosamente")
        print("\n Credenciales de prueba:")
        print("   Paciente: paciente1 / password123")
        print("   Doctor 1: doctor1 / password123 (Cardiología)")
        print("   Doctor 2: doctor2 / password123 (Pediatría)")
        print("   Doctor 3: doctor3 / password123 (Dermatología)")
        print("   Admin: admin / admin123")
    except Exception as e:
        print(f" Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()
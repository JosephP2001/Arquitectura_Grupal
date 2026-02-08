# backend/scripts/init_data.py

import sys
import os

# Agregar el directorio raíz al path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from src.config.database import get_session_local, init_db
from src.infrastructure.models.postgresql.models import (
    User, UserRole, Patient, Doctor, Specialty, Schedule, Appointment, AppointmentStatus
)
from datetime import datetime, time, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password con límite de 72 bytes para bcrypt"""
    # Truncar a 72 bytes para evitar error de bcrypt
    if len(password.encode('utf-8')) > 72:
        password = password[:72]
    return pwd_context.hash(password)


def create_sample_data():
    """Crea datos de prueba en la base de datos"""
    
    # Inicializar BD
    init_db()
    
    # Crear sesión
    SessionLocal = get_session_local()
    db: Session = SessionLocal()
    
    try:
        print("🔧 Creando datos de prueba...")
        
        # 1. Crear especialidades
        print("📋 Creando especialidades...")
        specialties_data = [
            {"name": "Cardiología", "description": "Especialista en corazón"},
            {"name": "Dermatología", "description": "Especialista en piel"},
            {"name": "Pediatría", "description": "Especialista en niños"},
            {"name": "Traumatología", "description": "Especialista en huesos"},
        ]
        
        specialties = []
        for spec_data in specialties_data:
            existing = db.query(Specialty).filter(Specialty.name == spec_data["name"]).first()
            if not existing:
                specialty = Specialty(**spec_data)
                db.add(specialty)
                specialties.append(specialty)
            else:
                specialties.append(existing)
        
        db.commit()
        print(f"✅ {len(specialties)} especialidades creadas")
        
        # 2. Crear usuarios admin
        print("👤 Creando usuario admin...")
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            admin_user = User(
                email="admin@hospital.com",
                username="admin",
                password_hash=hash_password("admin123"),
                full_name="Administrador del Sistema",
                role=UserRole.ADMIN,
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Usuario admin creado (usuario: admin, contraseña: admin123)")
        
        # 3. Crear pacientes de prueba
        print("🏥 Creando pacientes de prueba...")
        patients_data = [
            {
                "email": "paciente1@email.com",
                "username": "paciente1",
                "password": "pass123",
                "full_name": "Juan Pérez",
                "phone": "0998765432",
                "address": "Av. Principal 123"
            },
            {
                "email": "paciente2@email.com",
                "username": "paciente2",
                "password": "pass123",
                "full_name": "María García",
                "phone": "0987654321",
                "address": "Calle Secundaria 456"
            },
        ]
        
        for patient_data in patients_data:
            existing = db.query(User).filter(User.username == patient_data["username"]).first()
            if not existing:
                user = User(
                    email=patient_data["email"],
                    username=patient_data["username"],
                    password_hash=hash_password(patient_data["password"]),
                    full_name=patient_data["full_name"],
                    role=UserRole.PATIENT,
                    is_active=True
                )
                db.add(user)
                db.commit()
                
                patient = Patient(
                    user_id=user.id,
                    phone=patient_data["phone"],
                    address=patient_data["address"]
                )
                db.add(patient)
                db.commit()
        
        print("✅ Pacientes creados")
        
        # 4. Crear médicos de prueba
        print("👨‍⚕️ Creando médicos de prueba...")
        doctors_data = [
            {
                "email": "doctor1@hospital.com",
                "username": "doctor1",
                "password": "doc123",
                "full_name": "Dr. Carlos Rodríguez",
                "specialty": "Cardiología",
                "license": "LIC-001",
                "phone": "0991234567"
            },
            {
                "email": "doctor2@hospital.com",
                "username": "doctor2",
                "password": "doc123",
                "full_name": "Dra. Ana Martínez",
                "specialty": "Dermatología",
                "license": "LIC-002",
                "phone": "0992345678"
            },
        ]
        
        for doctor_data in doctors_data:
            existing = db.query(User).filter(User.username == doctor_data["username"]).first()
            if not existing:
                user = User(
                    email=doctor_data["email"],
                    username=doctor_data["username"],
                    password_hash=hash_password(doctor_data["password"]),
                    full_name=doctor_data["full_name"],
                    role=UserRole.DOCTOR,
                    is_active=True
                )
                db.add(user)
                db.commit()
                
                specialty = db.query(Specialty).filter(Specialty.name == doctor_data["specialty"]).first()
                
                doctor = Doctor(
                    user_id=user.id,
                    specialty_id=specialty.id,
                    license_number=doctor_data["license"],
                    phone=doctor_data["phone"]
                )
                db.add(doctor)
                db.commit()
                
                # Crear horarios para el médico
                for day in range(1, 6):  # Lunes a viernes
                    schedule = Schedule(
                        doctor_id=doctor.id,
                        day_of_week=day,
                        start_time=time(9, 0),
                        end_time=time(17, 0),
                        is_active=True
                    )
                    db.add(schedule)
                db.commit()
        
        print("✅ Médicos creados con horarios")
        
        print("\n" + "="*50)
        print("✅ DATOS DE PRUEBA CREADOS EXITOSAMENTE")
        print("="*50)
        print("\n📝 Credenciales de acceso:")
        print("\nAdministrador:")
        print("  Usuario: admin")
        print("  Contraseña: admin123")
        print("\nPacientes:")
        print("  Usuario: paciente1 / Contraseña: pass123")
        print("  Usuario: paciente2 / Contraseña: pass123")
        print("\nMédicos:")
        print("  Usuario: doctor1 / Contraseña: doc123")
        print("  Usuario: doctor2 / Contraseña: doc123")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error creando datos: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
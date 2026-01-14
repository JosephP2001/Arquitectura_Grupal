from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from src.infrastructure.dao.interfaces.appointment_dao import IAppointmentDAO
from src.infrastructure.models.postgresql.models import Appointment

class AppointmentDAOPostgreSQL(IAppointmentDAO):
    """Implementación de Appointment DAO para PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, appointment: Appointment) -> Appointment:
        """Crear una nueva cita"""
        self.db.add(appointment)
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def get_by_id(self, appointment_id: int) -> Optional[Appointment]:
        """Obtener cita por ID"""
        return self.db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()
    
    def get_by_patient(self, patient_id: int) -> List[Appointment]:
        """Obtener citas de un paciente"""
        return self.db.query(Appointment).filter(
            Appointment.patient_id == patient_id
        ).order_by(Appointment.appointment_date.desc()).all()
    
    def get_by_doctor(self, doctor_id: int) -> List[Appointment]:
        """Obtener citas de un médico"""
        return self.db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id
        ).order_by(Appointment.appointment_date.desc()).all()
    
    def get_by_date_range(
        self,
        doctor_id: int,
        start_date: datetime,
        end_date: datetime
    ) -> List[Appointment]:
        """Obtener citas en un rango de fechas"""
        return self.db.query(Appointment).filter(
            Appointment.doctor_id == doctor_id,
            Appointment.appointment_date >= start_date,
            Appointment.appointment_date <= end_date
        ).order_by(Appointment.appointment_date).all()
    
    def update(self, appointment: Appointment) -> Appointment:
        """Actualizar cita"""
        self.db.commit()
        self.db.refresh(appointment)
        return appointment
    
    def delete(self, appointment_id: int) -> bool:
        """Eliminar cita"""
        appointment = self.get_by_id(appointment_id)
        if appointment:
            self.db.delete(appointment)
            self.db.commit()
            return True
        return False
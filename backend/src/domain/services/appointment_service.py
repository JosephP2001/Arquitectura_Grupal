"""
Servicio de dominio: AppointmentService
Contiene la lógica de negocio relacionada con las citas
"""
from datetime import datetime
from typing import List, Optional
from src.domain.entities.appointment import AppointmentEntity

class AppointmentService:
    """Servicio para gestionar la lógica de negocio de citas"""
    
    @staticmethod
    def validate_appointment_date(appointment_date: datetime) -> tuple[bool, str]:
        """
        Valida que la fecha de la cita sea válida
        Reglas:
        - No puede ser en el pasado
        - Debe ser en horario laboral (8 AM - 8 PM)
        - No puede ser domingo
        """
        now = datetime.utcnow()
        
        # Validar que no sea en el pasado
        if appointment_date <= now:
            return False, "La cita no puede ser en el pasado"
        
        # Validar que sea en horario laboral
        hour = appointment_date.hour
        if hour < 8 or hour >= 20:
            return False, "La cita debe estar entre las 8:00 AM y las 8:00 PM"
        
        # Validar que no sea domingo (6)
        if appointment_date.weekday() == 6:
            return False, "No se pueden agendar citas los domingos"
        
        return True, "Fecha válida"
    
    @staticmethod
    def check_availability(
        doctor_id: int,
        appointment_date: datetime,
        duration_minutes: int,
        existing_appointments: List[AppointmentEntity]
    ) -> tuple[bool, str]:
        """
        Verifica si hay disponibilidad para una cita
        """
        # Crear entidad temporal para la nueva cita
        new_appointment = AppointmentEntity(
            id=None,
            patient_id=0,  # Temporal
            doctor_id=doctor_id,
            appointment_date=appointment_date,
            duration_minutes=duration_minutes,
            status="pending",
            reason=""
        )
        
        # Verificar conflictos con citas existentes
        for existing in existing_appointments:
            # Solo verificar citas activas (no canceladas)
            if existing.is_cancelled():
                continue
            
            if new_appointment.conflicts_with(existing):
                return False, f"Conflicto con cita existente a las {existing.appointment_date.strftime('%H:%M')}"
        
        return True, "Horario disponible"
    
    @staticmethod
    def can_cancel_appointment(appointment: AppointmentEntity) -> tuple[bool, str]:
        """
        Verifica si una cita puede ser cancelada
        Reglas:
        - No se puede cancelar si ya fue completada
        - Se debe cancelar con al menos 24 horas de anticipación
        """
        if appointment.is_completed():
            return False, "No se puede cancelar una cita completada"
        
        if appointment.is_cancelled():
            return False, "La cita ya está cancelada"
        
        # Verificar anticipación de 24 horas
        now = datetime.utcnow()
        hours_until_appointment = (appointment.appointment_date - now).total_seconds() / 3600
        
        if hours_until_appointment < 24:
            return False, "Debe cancelar con al menos 24 horas de anticipación"
        
        return True, "La cita puede ser cancelada"
    
    @staticmethod
    def calculate_appointment_statistics(appointments: List[AppointmentEntity]) -> dict:
        """
        Calcula estadísticas sobre las citas
        """
        total = len(appointments)
        if total == 0:
            return {
                "total": 0,
                "pending": 0,
                "confirmed": 0,
                "completed": 0,
                "cancelled": 0,
                "completion_rate": 0.0
            }
        
        pending = sum(1 for a in appointments if a.is_pending())
        confirmed = sum(1 for a in appointments if a.is_confirmed())
        completed = sum(1 for a in appointments if a.is_completed())
        cancelled = sum(1 for a in appointments if a.is_cancelled())
        
        completion_rate = (completed / total) * 100 if total > 0 else 0
        
        return {
            "total": total,
            "pending": pending,
            "confirmed": confirmed,
            "completed": completed,
            "cancelled": cancelled,
            "completion_rate": round(completion_rate, 2)
        }
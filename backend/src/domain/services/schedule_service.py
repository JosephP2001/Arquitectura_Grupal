"""
Servicio de dominio: ScheduleService
Contiene la lógica de negocio relacionada con los horarios
"""
from datetime import datetime, time
from typing import List
from src.domain.entities.schedule import ScheduleEntity

class ScheduleService:
    """Servicio para gestionar la lógica de negocio de horarios"""
    
    @staticmethod
    def validate_schedule(schedule: ScheduleEntity, existing_schedules: List[ScheduleEntity]) -> tuple[bool, str]:
        """
        Valida que un horario sea correcto y no tenga conflictos
        """
        # Validar el horario básico
        is_valid, message = schedule.validate()
        if not is_valid:
            return False, message
        
        # Verificar conflictos con horarios existentes del mismo médico
        for existing in existing_schedules:
            if existing.id == schedule.id:  # Ignorar el mismo horario en actualizaciones
                continue
            
            if not existing.is_active:  # Ignorar horarios inactivos
                continue
            
            if schedule.conflicts_with(existing):
                return False, f"Conflicto con horario existente el {existing.get_day_name()}"
        
        return True, "Horario válido"
    
    @staticmethod
    def get_available_time_slots(
        schedule: ScheduleEntity,
        slot_duration_minutes: int = 30
    ) -> List[time]:
        """
        Genera slots de tiempo disponibles basados en un horario
        """
        slots = []
        
        # Convertir times a datetime para poder hacer aritmética
        current = datetime.combine(datetime.today(), schedule.start_time)
        end = datetime.combine(datetime.today(), schedule.end_time)
        
        while current < end:
            slots.append(current.time())
            # Agregar duración del slot
            current = current.replace(minute=current.minute + slot_duration_minutes)
            # Manejar overflow de minutos
            if current.minute >= 60:
                current = current.replace(hour=current.hour + 1, minute=current.minute - 60)
        
        return slots
    
    @staticmethod
    def is_doctor_available_at_time(
        check_datetime: datetime,
        doctor_schedules: List[ScheduleEntity]
    ) -> bool:
        """
        Verifica si un médico está disponible en un momento específico
        """
        check_day = check_datetime.weekday()
        check_time = check_datetime.time()
        
        for schedule in doctor_schedules:
            if not schedule.is_active:
                continue
            
            if schedule.day_of_week == check_day:
                if schedule.is_time_in_range(check_time):
                    return True
        
        return False
    
    @staticmethod
    def get_weekly_hours(schedules: List[ScheduleEntity]) -> float:
        """
        Calcula el total de horas semanales de atención
        """
        total_hours = 0.0
        
        for schedule in schedules:
            if schedule.is_active:
                total_hours += schedule.get_duration_hours()
        
        return round(total_hours, 2)
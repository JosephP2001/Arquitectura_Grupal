from typing import Optional, List
from sqlalchemy.orm import Session
from src.infrastructure.models.postgresql.models import Schedule

class ScheduleDAOPostgreSQL:
    """Implementación de Schedule DAO para PostgreSQL"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, schedule: Schedule) -> Schedule:
        """Crear un nuevo horario"""
        self.db.add(schedule)
        self.db.commit()
        self.db.refresh(schedule)
        return schedule
    
    def get_by_id(self, schedule_id: int) -> Optional[Schedule]:
        """Obtener horario por ID"""
        return self.db.query(Schedule).filter(
            Schedule.id == schedule_id
        ).first()
    
    def get_by_doctor(self, doctor_id: int) -> List[Schedule]:
        """Obtener horarios de un médico"""
        return self.db.query(Schedule).filter(
            Schedule.doctor_id == doctor_id
        ).order_by(Schedule.day_of_week, Schedule.start_time).all()
    
    def get_active_by_doctor(self, doctor_id: int) -> List[Schedule]:
        """Obtener horarios activos de un médico"""
        return self.db.query(Schedule).filter(
            Schedule.doctor_id == doctor_id,
            Schedule.is_active == True
        ).order_by(Schedule.day_of_week, Schedule.start_time).all()
    
    def update(self, schedule: Schedule) -> Schedule:
        """Actualizar horario"""
        self.db.commit()
        self.db.refresh(schedule)
        return schedule
    
    def delete(self, schedule_id: int) -> bool:
        """Eliminar horario"""
        schedule = self.get_by_id(schedule_id)
        if schedule:
            self.db.delete(schedule)
            self.db.commit()
            return True
        return False
    
    def deactivate(self, schedule_id: int) -> bool:
        """Desactivar horario (soft delete)"""
        schedule = self.get_by_id(schedule_id)
        if schedule:
            schedule.is_active = False
            self.db.commit()
            return True
        return False
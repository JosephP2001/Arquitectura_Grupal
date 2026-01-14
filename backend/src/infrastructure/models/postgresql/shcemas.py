from datetime import datetime
from typing import Optional, List, Dict, Any

class MedicalRecord:
    """Esquema para historial médico en MongoDB"""
    
    def __init__(
        self,
        patient_id: int,
        doctor_id: int,
        appointment_id: int,
        diagnosis: str,
        treatment: str,
        observations: str,
        prescriptions: List[Dict[str, Any]] = None,
        created_at: datetime = None
    ):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_id = appointment_id
        self.diagnosis = diagnosis
        self.treatment = treatment
        self.observations = observations
        self.prescriptions = prescriptions or []
        self.created_at = created_at or datetime.utcnow()
    
    def to_dict(self):
        return {
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "appointment_id": self.appointment_id,
            "diagnosis": self.diagnosis,
            "treatment": self.treatment,
            "observations": self.observations,
            "prescriptions": self.prescriptions,
            "created_at": self.created_at
        }

class SystemLog:
    """Esquema para logs del sistema en MongoDB"""
    
    def __init__(
        self,
        level: str,
        message: str,
        user_id: Optional[int] = None,
        action: Optional[str] = None,
        metadata: Dict[str, Any] = None,
        timestamp: datetime = None
    ):
        self.level = level
        self.message = message
        self.user_id = user_id
        self.action = action
        self.metadata = metadata or {}
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self):
        return {
            "level": self.level,
            "message": self.message,
            "user_id": self.user_id,
            "action": self.action,
            "metadata": self.metadata,
            "timestamp": self.timestamp
        }
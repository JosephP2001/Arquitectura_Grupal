from typing import List, Optional
from pymongo.database import Database
from src.infrastructure.models.mongodb.schemas import MedicalRecord
from bson import ObjectId

class MedicalRecordDAOMongo:
    """DAO para gestionar historiales médicos en MongoDB"""
    
    def __init__(self, mongodb: Database):
        self.collection = mongodb.medical_records
    
    def create(self, record: MedicalRecord) -> str:
        """Crear un nuevo historial médico"""
        result = self.collection.insert_one(record.to_dict())
        return str(result.inserted_id)
    
    def get_by_id(self, record_id: str) -> Optional[dict]:
        """Obtener historial por ID"""
        return self.collection.find_one({"_id": ObjectId(record_id)})
    
    def get_by_patient(self, patient_id: int) -> List[dict]:
        """Obtener todos los historiales de un paciente"""
        return list(self.collection.find({"patient_id": patient_id}).sort("created_at", -1))
    
    def get_by_appointment(self, appointment_id: int) -> Optional[dict]:
        """Obtener historial por cita"""
        return self.collection.find_one({"appointment_id": appointment_id})
    
    def update(self, record_id: str, update_data: dict) -> bool:
        """Actualizar historial médico"""
        result = self.collection.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": update_data}
        )
        return result.modified_count > 0
    
    def delete(self, record_id: str) -> bool:
        """Eliminar historial médico"""
        result = self.collection.delete_one({"_id": ObjectId(record_id)})
        return result.deleted_count > 0
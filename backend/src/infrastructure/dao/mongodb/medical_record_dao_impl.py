from typing import List
from pymongo.database import Database
from datetime import datetime


class MedicalRecordDAOMongo:
    """DAO para gestionar registros médicos en MongoDB"""
    
    def __init__(self, mongodb: Database):
        self.collection = mongodb.medical_records
    
    def create(self, record: dict) -> str:
        """Crear un nuevo registro médico"""
        if 'created_at' not in record:
            record['created_at'] = datetime.utcnow()
        
        result = self.collection.insert_one(record)
        return str(result.inserted_id)
    
    def get_by_patient(self, patient_id: int) -> List[dict]:
        """Obtener registros médicos de un paciente"""
        records = list(
            self.collection
            .find({"patient_id": patient_id})
            .sort("created_at", -1)
        )
        
        for record in records:
            record['_id'] = str(record['_id'])
            if isinstance(record.get('created_at'), datetime):
                record['created_at'] = record['created_at'].isoformat()
        
        return records
    
    def get_by_appointment(self, appointment_id: int) -> dict:
        """Obtener registro médico de una cita"""
        record = self.collection.find_one({"appointment_id": appointment_id})
        
        if record:
            record['_id'] = str(record['_id'])
            if isinstance(record.get('created_at'), datetime):
                record['created_at'] = record['created_at'].isoformat()
        
        return record
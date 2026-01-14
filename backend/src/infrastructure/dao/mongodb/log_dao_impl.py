from typing import List
from pymongo.database import Database
from src.infrastructure.models.mongodb.schemas import SystemLog
from datetime import datetime, timedelta

class LogDAOMongo:
    """DAO para gestionar logs del sistema en MongoDB"""
    
    def __init__(self, mongodb: Database):
        self.collection = mongodb.system_logs
    
    def create(self, log: SystemLog) -> str:
        """Crear un nuevo log"""
        result = self.collection.insert_one(log.to_dict())
        return str(result.inserted_id)
    
    def get_by_user(self, user_id: int, limit: int = 100) -> List[dict]:
        """Obtener logs de un usuario"""
        return list(
            self.collection
            .find({"user_id": user_id})
            .sort("timestamp", -1)
            .limit(limit)
        )
    
    def get_by_level(self, level: str, limit: int = 100) -> List[dict]:
        """Obtener logs por nivel"""
        return list(
            self.collection
            .find({"level": level})
            .sort("timestamp", -1)
            .limit(limit)
        )
    
    def get_recent(self, hours: int = 24, limit: int = 100) -> List[dict]:
        """Obtener logs recientes"""
        since = datetime.utcnow() - timedelta(hours=hours)
        return list(
            self.collection
            .find({"timestamp": {"$gte": since}})
            .sort("timestamp", -1)
            .limit(limit)
        )
    
    def get_by_action(self, action: str, limit: int = 100) -> List[dict]:
        """Obtener logs por acción"""
        return list(
            self.collection
            .find({"action": action})
            .sort("timestamp", -1)
            .limit(limit)
        )
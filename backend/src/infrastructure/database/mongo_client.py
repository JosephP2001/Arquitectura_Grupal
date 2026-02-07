from pymongo import MongoClient

from src.infrastructure.registry.service_registry import service_registry
from src.infrastructure.resilience.circuit_breaker import CircuitBreaker


# --------------------------------------------------
# MongoDB (via Service Registry)
# --------------------------------------------------
mongo_srv = service_registry.get("mongo")

if not mongo_srv:
    raise RuntimeError("❌ MongoDB service not registered in Service Registry")

mongo_breaker = CircuitBreaker(fail_max=3, reset_timeout=30)


class MongoDatabase:
    def __init__(self):
        self.client = MongoClient(
            host=mongo_srv["host"],
            port=mongo_srv["port"],
            serverSelectionTimeoutMS=3000,
        )
        self.db = self.client["medical_reports"]

    @mongo_breaker
    def get_database(self):
        """
        Devuelve la base de datos MongoDB.
        Fuerza ping para detectar caída real del servicio.
        """
        self.client.admin.command("ping")
        return self.db


# Singleton
mongo_db = MongoDatabase()

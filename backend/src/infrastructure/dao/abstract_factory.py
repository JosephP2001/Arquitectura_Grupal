from abc import ABC, abstractmethod
from src.infrastructure.dao.interfaces.user_dao import IUserDAO
from src.infrastructure.dao.postgresql.user_dao_impl import UserDAOPostgreSQL
from src.infrastructure.dao.mongodb.medical_record_dao_impl import MedicalRecordDAOMongo
from src.infrastructure.dao.mongodb.log_dao_impl import LogDAOMongo

class DAOFactory(ABC):
    """Abstract Factory para crear DAOs"""
    
    @abstractmethod
    def create_user_dao(self) -> IUserDAO:
        pass
    
    @abstractmethod
    def create_medical_record_dao(self):
        pass
    
    @abstractmethod
    def create_log_dao(self):
        pass

class PostgreSQLDAOFactory(DAOFactory):
    """Factory para DAOs de PostgreSQL"""
    
    def __init__(self, db_session):
        self.db_session = db_session
    
    def create_user_dao(self) -> IUserDAO:
        return UserDAOPostgreSQL(self.db_session)
    
    def create_medical_record_dao(self):
        raise NotImplementedError("Medical records are stored in MongoDB")
    
    def create_log_dao(self):
        raise NotImplementedError("Logs are stored in MongoDB")

class MongoDBDAOFactory(DAOFactory):
    """Factory para DAOs de MongoDB"""
    
    def __init__(self, mongodb):
        self.mongodb = mongodb
    
    def create_user_dao(self) -> IUserDAO:
        raise NotImplementedError("Users are stored in PostgreSQL")
    
    def create_medical_record_dao(self):
        return MedicalRecordDAOMongo(self.mongodb)
    
    def create_log_dao(self):
        return LogDAOMongo(self.mongodb)

class HybridDAOFactory:
    """Factory híbrido que combina PostgreSQL y MongoDB"""
    
    def __init__(self, db_session, mongodb):
        self.postgres_factory = PostgreSQLDAOFactory(db_session)
        self.mongo_factory = MongoDBDAOFactory(mongodb)
    
    def create_user_dao(self) -> IUserDAO:
        return self.postgres_factory.create_user_dao()
    
    def create_medical_record_dao(self):
        return self.mongo_factory.create_medical_record_dao()
    
    def create_log_dao(self):
        return self.mongo_factory.create_log_dao()
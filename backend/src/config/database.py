from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pymongo import MongoClient
from src.infrastructure.registry.service_registry import service_registry
import os

# Definir Base para las clases ORM de SQLAlchemy
Base = declarative_base()

# Variables globales
_engine = None
_SessionLocal = None
_mongo_client = None
_mongo_db = None

def _init_postgres():
    """Inicializa PostgreSQL usando Service Registry"""
    global _engine, _SessionLocal

    if _engine is not None:
        return

    try:
        pg = service_registry.get("postgres")
        DATABASE_URL = (
            f"postgresql://medical_user:medical_pass@"
            f"{pg['host']}:{pg['port']}/medical_appointments"
        )
    except:
        # Fallback para desarrollo local
        DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://medical_user:medical_pass@localhost:5432/medical_appointments"
        )

    _engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


def _init_mongodb():
    """Inicializa MongoDB usando Service Registry"""
    global _mongo_client, _mongo_db

    if _mongo_client is not None:
        return

    try:
        mongo = service_registry.get("mongo")
        _mongo_client = MongoClient(
            host=mongo['host'],
            port=mongo['port'],
            username="mongo_user",
            password="mongo_pass",
            serverSelectionTimeoutMS=3000
        )
    except:
        # Fallback para desarrollo local
        mongodb_url = os.getenv(
            "MONGODB_URL",
            "mongodb://mongo_user:mongo_pass@localhost:27017/"
        )
        _mongo_client = MongoClient(
            mongodb_url,
            serverSelectionTimeoutMS=3000
        )
    
    _mongo_db = _mongo_client["medical_records"]


def get_engine():
    """Devuelve el motor de PostgreSQL"""
    if _engine is None:
        _init_postgres()
    return _engine


def get_session_local():
    """Devuelve el session maker de PostgreSQL"""
    if _SessionLocal is None:
        _init_postgres()
    return _SessionLocal


def get_db():
    """Generador de sesiones de PostgreSQL para FastAPI"""
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def get_mongodb():
    """Devuelve la base de datos de MongoDB"""
    if _mongo_db is None:
        _init_mongodb()
    return _mongo_db


def init_db():
    """Inicializa tablas de PostgreSQL"""
    from src.infrastructure.models.postgresql.models import Base

    engine = get_engine()
    Base.metadata.create_all(bind=engine)
    print("✅ PostgreSQL tables created using Service Registry")
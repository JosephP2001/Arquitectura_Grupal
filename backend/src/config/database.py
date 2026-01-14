from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from src.config.settings import settings

# PostgreSQL Configuration
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# MongoDB Configuration
mongo_client = MongoClient(settings.MONGODB_URL)
mongodb = mongo_client[settings.MONGODB_DB_NAME]

def get_db():
    """Dependency para obtener sesión de PostgreSQL"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_mongodb():
    """Dependency para obtener conexión de MongoDB"""
    return mongodb

def init_db():
    """Inicializar bases de datos"""
    # Crear tablas en PostgreSQL
    from src.infrastructure.models.postgresql.models import Base
    Base.metadata.create_all(bind=engine)
    
    print("✅ PostgreSQL tables created")
    print("✅ MongoDB connection established")
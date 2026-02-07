from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

from src.infrastructure.registry.service_registry import service_registry
from src.config.settings import settings


# --------------------------------------------------
# PostgreSQL (via Service Registry)
# --------------------------------------------------
pg = service_registry.get("postgres")

if not pg:
    raise RuntimeError("❌ PostgreSQL service not registered in Service Registry")

DATABASE_URL = (
    f"postgresql://medical_user:medical_pass@"
    f"{pg['host']}:{pg['port']}/medical_appointments"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# --------------------------------------------------
# MongoDB (todavía usando settings)
# (opcionalmente luego se migra al registry)
# --------------------------------------------------
mongo_client = MongoClient(settings.MONGODB_URL)
mongodb = mongo_client[settings.MONGODB_DB_NAME]


# --------------------------------------------------
# Dependencies
# --------------------------------------------------
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


# --------------------------------------------------
# Init DB
# --------------------------------------------------
def init_db():
    """Inicializar bases de datos"""
    from src.infrastructure.models.postgresql.models import Base

    Base.metadata.create_all(bind=engine)

    print("✅ PostgreSQL tables created using Service Registry")
    print("✅ MongoDB connection established")

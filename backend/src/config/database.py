from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.infrastructure.registry.service_registry import service_registry

# Definir Base para las clases ORM de SQLAlchemy
Base = declarative_base()

# Variables globales para el engine y la session
_engine = None
_SessionLocal = None

def _init_postgres():
    """
    Inicializa el motor de base de datos y la session
    usando información de servicio de la configuración
    """
    global _engine, _SessionLocal

    # Solo inicializar si aún no se ha hecho
    if _engine is not None:
        return

    # Obtener la configuración del servicio de postgres
    pg = service_registry.get("postgres")

    # Construir la URL de conexión a la base de datos
    DATABASE_URL = (
        f"postgresql://medical_user:medical_pass@"
        f"{pg['host']}:{pg['port']}/medical_appointments"
    )

    # Crear el motor de la base de datos
    _engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

    # Crear el session maker para conectar a la base de datos
    _SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_engine,
    )


def get_engine():
    """
    Devuelve el motor de la base de datos
    Inicializa si aún no está configurado
    """
    if _engine is None:
        _init_postgres()
    return _engine


def get_session_local():
    """
    Devuelve el session maker configurado para crear sesiones
    """
    if _SessionLocal is None:
        _init_postgres()
    return _SessionLocal


def get_db():
    """
    Generador que crea y cierra sesiones de base de datos
    Útil para inyectar dependencias en FastAPI
    """
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializa las tablas de la base de datos PostgreSQL.
    Se debe llamar en el startup cuando el registro de servicios esté listo.
    """
    from src.infrastructure.models.postgresql.models import Base

    # Obtener el motor de la base de datos
    engine = get_engine()

    # Crear todas las tablas que no existan
    Base.metadata.create_all(bind=engine)

    print("✅ PostgreSQL tables created using Service Registry")

def get_mongodb():
    raise NotImplementedError("MongoDB client not initialized yet")


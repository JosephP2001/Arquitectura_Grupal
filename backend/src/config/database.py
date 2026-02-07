from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.infrastructure.registry.service_registry import service_registry


Base = declarative_base()

_engine = None
_SessionLocal = None


def _init_postgres():
    global _engine, _SessionLocal

    if _engine is not None:
        return

    pg = service_registry.get("postgres")

    DATABASE_URL = (
        f"postgresql://medical_user:medical_pass@"
        f"{pg['host']}:{pg['port']}/medical_appointments"
    )

    _engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
    )

    _SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=_engine,
    )


def get_engine():
    if _engine is None:
        _init_postgres()
    return _engine


def get_session_local():
    if _SessionLocal is None:
        _init_postgres()
    return _SessionLocal


def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Inicializar tablas PostgreSQL
    (se llama en startup, cuando el registry ya está listo)
    """
    from src.infrastructure.models.postgresql.models import Base

    engine = get_engine()
    Base.metadata.create_all(bind=engine)

    print("✅ PostgreSQL tables created using Service Registry")

import threading
import time
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis

# Importar funciones y servicios
from src.config.database import init_db
from src.infrastructure.registry.service_registry import service_registry
from src.presentation.routes.auth_routes import router as auth_router
from src.presentation.routes.appointment_routes import router as appointment_router
from src.presentation.routes.doctor_routes import router as doctor_router
from src.presentation.routes.patient_routes import router as patient_router
from src.presentation.routes.report_routes import router as report_router
from src.presentation.middlewares.error_logging_middleware import ErrorLoggingMiddleware

# --------------------------------------------------
# Configuración de la aplicación FastAPI
# --------------------------------------------------
app = FastAPI(
    title="Medical Appointment Platform API",
    description="API para gestión de citas médicas",
    version="1.0.0"
)

# --------------------------------------------------
# Middlewares
# --------------------------------------------------
app.add_middleware(ErrorLoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Heartbeat loop para registrar la salud de los servicios
# --------------------------------------------------
def heartbeat_loop(interval: int = 10):
    """
    Envía heartbeats periódicos al Service Registry
    """
    while True:
        service_registry.heartbeat("postgres")
        service_registry.heartbeat("redis")
        service_registry.heartbeat("mongo")
        time.sleep(interval)

# --------------------------------------------------
# Evento de inicio (Startup)
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    # 1. Registrar los servicios primero (sin consumirlos)
    service_registry.register(
        name="postgres",
        host="medical_postgres",  # Nombre del contenedor de Postgres en Docker
        port=5432
    )

    service_registry.register(
        name="mongo",
        host="medical_mongo",  # Nombre del contenedor de MongoDB en Docker
        port=27017
    )

    service_registry.register(
        name="redis",
        host="medical_redis",  # Nombre del contenedor de Redis en Docker
        port=6379
    )

    # 2. Inicializar la base de datos (ahora se puede consumir postgres)
    init_db()

    # 3. Iniciar heartbeat en segundo plano
    threading.Thread(
        target=heartbeat_loop,
        daemon=True
    ).start()

# --------------------------------------------------
# Rutas de la API
# --------------------------------------------------
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])

# --------------------------------------------------
# Rutas de estado (Health Check y Root)
# --------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Medical Appointment Platform API V1",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

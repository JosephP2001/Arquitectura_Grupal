import threading
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.database import init_db
from src.infrastructure.registry.service_registry import service_registry

from src.presentation.routes.auth_routes import router as auth_router
from src.presentation.routes.appointment_routes import router as appointment_router
from src.presentation.routes.doctor_routes import router as doctor_router
from src.presentation.routes.patient_routes import router as patient_router
from src.presentation.routes.report_routes import router as report_router
from src.presentation.middlewares.error_logging_middleware import ErrorLoggingMiddleware


# --------------------------------------------------
# App
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
# Heartbeat loop
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
# Startup
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    # Inicializar base de datos
    init_db()

    # Registrar servicios
    service_registry.register(
        name="postgres",
        host="medical_postgres",
        port=5432
    )

    service_registry.register(
        name="redis",
        host="medical_redis",
        port=6379
    )

    service_registry.register(
        name="mongo",
        host="medical_mongo",
        port=27017
    )

    # Iniciar heartbeat en background
    threading.Thread(
        target=heartbeat_loop,
        daemon=True
    ).start()


# --------------------------------------------------
# Routes
# --------------------------------------------------
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])


# --------------------------------------------------
# Root & Health
# --------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Medical Appointment Platform API",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

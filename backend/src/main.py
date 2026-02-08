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
# Configuración de la aplicación FastAPI
# --------------------------------------------------
app = FastAPI(
    title="Medical Appointment Platform API",
    description="API para gestión de citas médicas con Service Registry y Circuit Breaker",
    version="1.0.0"
)

# --------------------------------------------------
# Middlewares - CORS debe ir PRIMERO
# --------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
        "http://medical_frontend:5173",  # Nombre del contenedor
        # Para acceso en LAN - permitir todas las IPs locales
        "http://192.168.*.*:5173",
        "http://192.168.*.*:3000",
        "http://10.*.*.*:5173",
        "http://10.*.*.*:3000",
        "http://172.*.*.*:5173",
        "http://172.*.*.*:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    # Permitir orígenes con patrón (para LAN)
    allow_origin_regex=r"http://(192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\.\d+\.\d+\.\d+):(5173|3000|8000)"
)

app.add_middleware(ErrorLoggingMiddleware)

# --------------------------------------------------
# Heartbeat loop para Service Registry
# --------------------------------------------------
def heartbeat_loop(interval: int = 10):
    """Envía heartbeats periódicos al Service Registry"""
    while True:
        try:
            service_registry.heartbeat("postgres")
            service_registry.heartbeat("redis")
            service_registry.heartbeat("mongo")
        except Exception as e:
            print(f"⚠️ Error en heartbeat: {e}")
        time.sleep(interval)

# --------------------------------------------------
# Evento de inicio (Startup)
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    print("🚀 Iniciando Medical Appointment Platform...")
    
    # 1. Registrar servicios en Service Registry (Patrón 1)
    print("📦 Registrando servicios en Service Registry...")
    
    # Para producción (Docker)
    service_registry.register(
        name="postgres",
        host="postgres",  # Nombre del servicio en docker-compose
        port=5432
    )
    print("✅ PostgreSQL registrado")

    service_registry.register(
        name="mongo",
        host="mongodb",  # Nombre del servicio en docker-compose
        port=27017
    )
    print("✅ MongoDB registrado")

    service_registry.register(
        name="redis",
        host="redis",  # Nombre del servicio en docker-compose
        port=6379
    )
    print("✅ Redis registrado")

    # 2. Inicializar base de datos
    print("🗄️ Inicializando base de datos...")
    init_db()

    # 3. Iniciar heartbeat en segundo plano
    print("💓 Iniciando heartbeat del Service Registry...")
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    
    print("✅ Aplicación iniciada correctamente")
    print("🌐 Accesible en LAN - CORS configurado")

# --------------------------------------------------
# Rutas de la API
# --------------------------------------------------
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])

# --------------------------------------------------
# Rutas de estado
# --------------------------------------------------
@app.get("/")
async def root():
    return {
        "message": "Medical Appointment Platform API V1",
        "status": "running",
        "patterns": ["Service Registry", "Circuit Breaker"],
        "network": "LAN accessible"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    services_status = {}
    
    try:
        postgres = service_registry.get("postgres")
        services_status["postgres"] = postgres["status"]
    except:
        services_status["postgres"] = "DOWN"
    
    try:
        mongo = service_registry.get("mongo")
        services_status["mongo"] = mongo["status"]
    except:
        services_status["mongo"] = "DOWN"
    
    try:
        redis = service_registry.get("redis")
        services_status["redis"] = redis["status"]
    except:
        services_status["redis"] = "DOWN"
    
    return {
        "status": "healthy",
        "services": services_status
    }
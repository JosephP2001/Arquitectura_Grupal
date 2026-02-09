"""
Medical Appointment Platform - Main Application
FastAPI con Service Registry y Circuit Breaker
"""
import threading
import time
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configuración de base de datos
from src.config.database import init_db

# Service Registry y Notificaciones
from src.infrastructure.registry.service_registry import service_registry
from src.infrastructure.registry.notification_service import notification_service

# Rutas
from src.presentation.routes.auth_routes import router as auth_router
from src.presentation.routes.appointment_routes import router as appointment_router
from src.presentation.routes.doctor_routes import router as doctor_router
from src.presentation.routes.patient_routes import router as patient_router
from src.presentation.routes.report_routes import router as report_router

# Nuevas rutas para monitoreo y demo
from src.presentation.routes.monitoring_routes import router as monitoring_router
from src.presentation.routes.demo_routes import router as demo_router

# Middlewares
from src.presentation.middlewares.error_logging_middleware import ErrorLoggingMiddleware

# --------------------------------------------------
# Configuración de la aplicación FastAPI
# --------------------------------------------------
app = FastAPI(
    title="Medical Appointment Platform API",
    description="""
    API para gestión de citas médicas con patrones empresariales:
    
    **Patrones Implementados:**
    - 🔍 Service Registry con monitoreo y notificaciones
    - 🔌 Circuit Breaker con dashboard en tiempo real
    - 📊 DAO Pattern (Data Access Object)
    - 📦 DTO Pattern (Data Transfer Object)
    - 🏗️ Repository Pattern
    - 💉 Dependency Injection
    
    **Características:**
    - Monitoreo de servicios en tiempo real
    - Health checks automáticos
    - Notificaciones por email (SendGrid)
    - Dashboard interactivo
    - WebSocket para actualizaciones live
    """,
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
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
        "http://medical_frontend:5173",
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
# Heartbeat y Health Check loops
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


def health_check_loop(interval: int = 30):
    """Ejecuta health checks periódicos de todos los servicios"""
    while True:
        try:
            time.sleep(interval)  # Esperar antes del primer check
            print("🏥 Ejecutando health checks automáticos...")
            results = service_registry.health_check_all()
            
            # Log de resultados
            for service_name, is_healthy in results.items():
                status = "✅ UP" if is_healthy else "❌ DOWN"
                print(f"   {service_name}: {status}")
                
        except Exception as e:
            print(f"⚠️ Error en health check loop: {e}")


# --------------------------------------------------
# Evento de inicio (Startup)
# --------------------------------------------------
@app.on_event("startup")
async def startup_event():
    print("=" * 60)
    print("🚀 INICIANDO MEDICAL APPOINTMENT PLATFORM v2.0")
    print("=" * 60)
    
    # 1. Configurar Service Registry con MongoDB
    print("\n📦 Configurando Service Registry...")
    mongodb_url = os.getenv("MONGODB_URL", "mongodb://mongo_user:mongo_pass@mongodb:27017/")
    mongodb_db = os.getenv("MONGODB_DB_NAME", "medical_records")
    
    service_registry.set_mongodb_client(mongodb_url, mongodb_db)
    
    # 2. Configurar servicio de notificaciones
    print("📧 Configurando servicio de notificaciones...")
    service_registry.set_notification_service(notification_service)
    
    # 3. Registrar servicios en Service Registry
    print("\n🔍 Registrando servicios en Service Registry...")
    
    # PostgreSQL
    service_registry.register(
        name="postgres",
        host="postgres",
        port=5432,
        metadata={
            "type": "database",
            "engine": "PostgreSQL 15",
            "purpose": "Relational data storage"
        }
    )
    print("✅ PostgreSQL registrado")

    # MongoDB
    service_registry.register(
        name="mongo",
        host="mongodb",
        port=27017,
        metadata={
            "type": "database",
            "engine": "MongoDB 7",
            "purpose": "NoSQL document storage"
        }
    )
    print("✅ MongoDB registrado")

    # Redis
    service_registry.register(
        name="redis",
        host="redis",
        port=6379,
        metadata={
            "type": "cache",
            "engine": "Redis 7",
            "purpose": "Session storage and caching"
        }
    )
    print("✅ Redis registrado")

    # 4. Inicializar base de datos
    print("\n🗄️ Inicializando base de datos PostgreSQL...")
    init_db()
    print("✅ Base de datos inicializada")

    # 5. Iniciar heartbeat en segundo plano
    print("\n💓 Iniciando heartbeat loop (10s)...")
    threading.Thread(target=heartbeat_loop, daemon=True).start()
    
    # 6. Iniciar health checks automáticos en segundo plano
    print("🏥 Iniciando health check loop (30s)...")
    health_check_interval = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
    threading.Thread(
        target=health_check_loop,
        args=(health_check_interval,),
        daemon=True
    ).start()
    
    print("\n" + "=" * 60)
    print("✅ APLICACIÓN INICIADA CORRECTAMENTE")
    print("=" * 60)
    print("\n📊 Dashboards disponibles:")
    print("   - Service Registry: http://localhost:8000/docs#/Reports")
    print("   - Circuit Breaker: http://localhost:8000/docs#/Demo")
    print("   - WebSocket Monitoring: ws://localhost:8000/monitoring/ws/monitoring")
    print("\n🌐 Accesible en LAN - CORS configurado")
    print("=" * 60 + "\n")


# --------------------------------------------------
# Rutas de la API
# --------------------------------------------------

# Rutas existentes
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])

# Rutas nuevas de monitoreo
app.include_router(monitoring_router, prefix="/monitoring", tags=["Monitoring"])

# Rutas de demostración de Circuit Breaker
app.include_router(demo_router, prefix="/demo", tags=["Demo"])

# --------------------------------------------------
# Rutas de estado
# --------------------------------------------------
@app.get("/", tags=["Root"])
async def root():
    """Endpoint raíz con información del sistema"""
    return {
        "message": "Medical Appointment Platform API V2.0",
        "status": "running",
        "features": {
            "patterns": [
                "Service Registry",
                "Circuit Breaker",
                "DAO Pattern",
                "DTO Pattern",
                "Repository Pattern",
                "Dependency Injection"
            ],
            "monitoring": [
                "Health Checks",
                "Metrics Tracking",
                "Email Notifications",
                "WebSocket Live Updates"
            ]
        },
        "network": "LAN accessible",
        "documentation": {
            "swagger": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint del sistema completo
    
    Returns:
        Estado de salud de todos los servicios
    """
    services_status = {}
    overall_status = "healthy"
    
    # Verificar cada servicio
    for service_name in ["postgres", "mongo", "redis"]:
        try:
            service = service_registry.get(service_name)
            services_status[service_name] = {
                "status": service["status"],
                "last_check": service.get("last_check").isoformat() if service.get("last_check") else None
            }
            
            # Si algún servicio está DOWN, el sistema está degradado
            if service["status"] == "DOWN":
                overall_status = "degraded"
                
        except Exception as e:
            services_status[service_name] = {
                "status": "UNKNOWN",
                "error": str(e)
            }
            overall_status = "degraded"
    
    return {
        "status": overall_status,
        "services": services_status,
        "timestamp": time.time()
    }


@app.get("/info", tags=["Info"])
async def system_info():
    """
    Información del sistema y configuración
    
    Returns:
        Información detallada del sistema
    """
    return {
        "application": {
            "name": "Medical Appointment Platform",
            "version": "2.0.0",
            "environment": os.getenv("DEBUG", "False")
        },
        "patterns": {
            "service_registry": {
                "enabled": True,
                "services_registered": len(service_registry.get_all()),
                "health_check_interval": int(os.getenv("HEALTH_CHECK_INTERVAL", "30")),
                "notification_service": notification_service is not None
            },
            "circuit_breaker": {
                "enabled": True,
                "default_failure_threshold": int(os.getenv("CIRCUIT_BREAKER_FAILURE_THRESHOLD", "5")),
                "default_timeout": int(os.getenv("CIRCUIT_BREAKER_TIMEOUT", "30"))
            }
        },
        "configuration": {
            "session_expire_minutes": int(os.getenv("SESSION_EXPIRE_MINUTES", "60")),
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
            "lan_host_ip": os.getenv("LAN_HOST_IP", "192.168.1.7")
        }
    }
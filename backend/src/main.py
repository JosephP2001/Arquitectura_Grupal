from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.database import init_db
from src.presentation.routes.auth_routes import router as auth_router
from src.presentation.routes.appointment_routes import router as appointment_router
from src.presentation.routes.doctor_routes import router as doctor_router
from src.presentation.routes.patient_routes import router as patient_router
from src.presentation.routes.report_routes import router as report_router

app = FastAPI(
    title="Medical Appointment Platform API",
    description="API para gestión de citas médicas",
    version="1.0.0"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializar bases de datos
@app.on_event("startup")
async def startup_event():
    init_db()

# Rutas
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(appointment_router, prefix="/api/appointments", tags=["Appointments"])
app.include_router(doctor_router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(patient_router, prefix="/api/patients", tags=["Patients"])
app.include_router(report_router, prefix="/api/reports", tags=["Reports"])

@app.get("/")
async def root():
    return {"message": "Medical Appointment Platform API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
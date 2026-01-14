from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://medical_user:medical_pass@localhost:5432/medical_appointments"
    MONGODB_URL: str = "mongodb://mongo_user:mongo_pass@localhost:27017/"
    MONGODB_DB_NAME: str = "medical_records"
    
    # JWT
    JWT_SECRET: str = "your-super-secret-jwt-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application
    PROJECT_NAME: str = "Medical Appointment Platform"
    VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
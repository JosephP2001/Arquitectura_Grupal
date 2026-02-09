"""
Modelo MongoDB para el historial de estados de servicios
Usado por el Service Registry para tracking histórico
"""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class ServiceHealthCheck(BaseModel):
    """Modelo para un registro de health check"""
    service_name: str
    status: str  # "UP", "DOWN", "DEGRADED"
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    response_time_ms: Optional[float] = None
    error_message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "postgres",
                "status": "UP",
                "timestamp": "2026-02-08T19:30:00Z",
                "response_time_ms": 15.5,
                "error_message": None,
                "metadata": {
                    "host": "postgres",
                    "port": 5432,
                    "version": "15.0"
                }
            }
        }


class ServiceStatusChange(BaseModel):
    """Modelo para cambios de estado de servicios"""
    service_name: str
    previous_status: str
    new_status: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    reason: Optional[str] = None
    notification_sent: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "mongodb",
                "previous_status": "UP",
                "new_status": "DOWN",
                "timestamp": "2026-02-08T19:35:00Z",
                "reason": "Connection timeout",
                "notification_sent": True
            }
        }


class ServiceMetrics(BaseModel):
    """Modelo para métricas agregadas de un servicio"""
    service_name: str
    period_start: datetime
    period_end: datetime
    total_checks: int = 0
    successful_checks: int = 0
    failed_checks: int = 0
    average_response_time_ms: Optional[float] = None
    uptime_percentage: float = 0.0
    downtime_minutes: float = 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "service_name": "redis",
                "period_start": "2026-02-08T00:00:00Z",
                "period_end": "2026-02-08T23:59:59Z",
                "total_checks": 288,
                "successful_checks": 286,
                "failed_checks": 2,
                "average_response_time_ms": 12.3,
                "uptime_percentage": 99.3,
                "downtime_minutes": 10.5
            }
        }
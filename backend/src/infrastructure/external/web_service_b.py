"""
Servicio Web B - Simulador de Fallos
Este servicio simula un servicio externo que puede fallar intermitentemente
Usado para demostración del Circuit Breaker
"""
import random
import time
from typing import Dict, Any, Optional
from datetime import datetime


class WebServiceB:
    """
    Simulador de servicio externo con fallos controlados
    
    Modos de operación:
    - STABLE: Siempre responde correctamente
    - INTERMITTENT: Falla aleatoriamente (configurable)
    - FAILING: Siempre falla
    - SLOW: Responde lentamente (simula timeout)
    """
    
    def __init__(self):
        self.mode = "STABLE"
        self.failure_rate = 0.5  # 50% de fallos en modo INTERMITTENT
        self.slow_delay = 3.0    # Segundos de delay en modo SLOW
        
        # Estadísticas
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.last_request_time: Optional[datetime] = None
        
        print("🌐 Web Service B inicializado (modo: STABLE)")
    
    def set_mode(self, mode: str, **kwargs):
        """
        Configurar modo de operación
        
        Args:
            mode: STABLE, INTERMITTENT, FAILING, SLOW
            **kwargs: Parámetros adicionales (failure_rate, slow_delay)
        """
        valid_modes = ["STABLE", "INTERMITTENT", "FAILING", "SLOW"]
        if mode not in valid_modes:
            raise ValueError(f"Modo inválido. Usar: {valid_modes}")
        
        old_mode = self.mode
        self.mode = mode
        
        # Actualizar parámetros opcionales
        if "failure_rate" in kwargs:
            self.failure_rate = min(max(kwargs["failure_rate"], 0.0), 1.0)
        
        if "slow_delay" in kwargs:
            self.slow_delay = max(kwargs["slow_delay"], 0.0)
        
        print(f"🔧 Web Service B: {old_mode} → {mode}")
        
        if mode == "INTERMITTENT":
            print(f"   - Failure rate: {self.failure_rate * 100}%")
        elif mode == "SLOW":
            print(f"   - Delay: {self.slow_delay}s")
    
    def get_patient_data(self, patient_id: int) -> Dict[str, Any]:
        """
        Simular obtención de datos de paciente
        
        Args:
            patient_id: ID del paciente
        
        Returns:
            Datos del paciente
        
        Raises:
            Exception: Si el servicio está configurado para fallar
        """
        self.total_requests += 1
        self.last_request_time = datetime.utcnow()
        
        # Simular comportamiento según modo
        if self.mode == "FAILING":
            self.failed_requests += 1
            raise Exception("Service B is in FAILING mode - All requests fail")
        
        elif self.mode == "INTERMITTENT":
            if random.random() < self.failure_rate:
                self.failed_requests += 1
                raise Exception(f"Service B intermittent failure (rate: {self.failure_rate})")
        
        elif self.mode == "SLOW":
            time.sleep(self.slow_delay)
        
        # Respuesta exitosa
        self.successful_requests += 1
        
        return {
            "patient_id": patient_id,
            "name": f"Patient {patient_id}",
            "age": random.randint(18, 80),
            "last_visit": "2026-01-15",
            "conditions": ["Diabetes", "Hypertension"] if patient_id % 2 == 0 else [],
            "service_b_mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_appointment_slots(self, doctor_id: int, date: str) -> Dict[str, Any]:
        """
        Simular obtención de slots disponibles
        
        Args:
            doctor_id: ID del doctor
            date: Fecha en formato YYYY-MM-DD
        
        Returns:
            Slots disponibles
        
        Raises:
            Exception: Si el servicio está configurado para fallar
        """
        self.total_requests += 1
        self.last_request_time = datetime.utcnow()
        
        # Simular comportamiento según modo
        if self.mode == "FAILING":
            self.failed_requests += 1
            raise Exception("Service B is in FAILING mode")
        
        elif self.mode == "INTERMITTENT":
            if random.random() < self.failure_rate:
                self.failed_requests += 1
                raise Exception("Service B intermittent failure")
        
        elif self.mode == "SLOW":
            time.sleep(self.slow_delay)
        
        # Respuesta exitosa
        self.successful_requests += 1
        
        return {
            "doctor_id": doctor_id,
            "date": date,
            "available_slots": [
                "09:00", "10:00", "11:00", "14:00", "15:00", "16:00"
            ],
            "service_b_mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def send_notification(self, patient_id: int, message: str) -> Dict[str, Any]:
        """
        Simular envío de notificación
        
        Args:
            patient_id: ID del paciente
            message: Mensaje a enviar
        
        Returns:
            Confirmación de envío
        
        Raises:
            Exception: Si el servicio está configurado para fallar
        """
        self.total_requests += 1
        self.last_request_time = datetime.utcnow()
        
        # Simular comportamiento según modo
        if self.mode == "FAILING":
            self.failed_requests += 1
            raise Exception("Service B is in FAILING mode")
        
        elif self.mode == "INTERMITTENT":
            if random.random() < self.failure_rate:
                self.failed_requests += 1
                raise Exception("Service B intermittent failure")
        
        elif self.mode == "SLOW":
            time.sleep(self.slow_delay)
        
        # Respuesta exitosa
        self.successful_requests += 1
        
        return {
            "patient_id": patient_id,
            "message": message,
            "sent": True,
            "service_b_mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Obtener estadísticas del servicio"""
        success_rate = 0.0
        if self.total_requests > 0:
            success_rate = (self.successful_requests / self.total_requests) * 100
        
        return {
            "mode": self.mode,
            "configuration": {
                "failure_rate": self.failure_rate if self.mode == "INTERMITTENT" else None,
                "slow_delay": self.slow_delay if self.mode == "SLOW" else None
            },
            "statistics": {
                "total_requests": self.total_requests,
                "successful_requests": self.successful_requests,
                "failed_requests": self.failed_requests,
                "success_rate": round(success_rate, 2)
            },
            "last_request": self.last_request_time.isoformat() if self.last_request_time else None
        }
    
    def reset_statistics(self):
        """Resetear estadísticas"""
        self.total_requests = 0
        self.successful_requests = 0
        self.failed_requests = 0
        self.last_request_time = None
        print("📊 Estadísticas de Service B reseteadas")
    
    def health_check(self) -> Dict[str, Any]:
        """Health check del servicio"""
        return {
            "status": "UP" if self.mode != "FAILING" else "DOWN",
            "mode": self.mode,
            "timestamp": datetime.utcnow().isoformat()
        }


# Singleton
web_service_b = WebServiceB()
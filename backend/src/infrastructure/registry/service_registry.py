"""
Service Registry Mejorado con Monitoreo y Notificaciones
Patrón: Service Registry con Health Monitoring
"""
import time
import socket
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Any
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os


class ServiceRegistry:
    """
    Service Registry con funcionalidades avanzadas:
    - Registro dinámico de servicios
    - Health checks automáticos
    - Historial de estados en MongoDB
    - Notificaciones de cambios de estado
    """
    
    def __init__(self):
        self._services: Dict[str, Dict[str, Any]] = {}
        self._health_history: List[Dict[str, Any]] = []
        self._mongodb_client: Optional[MongoClient] = None
        self._mongo_db = None
        self._notification_service = None
        
        # Configuración
        self.health_check_interval = int(os.getenv("HEALTH_CHECK_INTERVAL", "30"))
        self.failure_threshold = int(os.getenv("FAILURE_THRESHOLD", "3"))
        
        print("🏥 Service Registry inicializado")
    
    def set_notification_service(self, notification_service):
        """Configurar servicio de notificaciones"""
        self._notification_service = notification_service
        print("📧 Servicio de notificaciones configurado")
    
    def set_mongodb_client(self, mongodb_url: str, db_name: str = "medical_records"):
        """
        Configurar cliente MongoDB para almacenar historial
        
        Args:
            mongodb_url: URL de conexión a MongoDB
            db_name: Nombre de la base de datos
        """
        try:
            self._mongodb_client = MongoClient(
                mongodb_url,
                serverSelectionTimeoutMS=5000
            )
            # Verificar conexión
            self._mongodb_client.admin.command('ping')
            self._mongo_db = self._mongodb_client[db_name]
            print(f"✅ MongoDB configurado para historial de servicios")
        except Exception as e:
            print(f"⚠️ No se pudo conectar a MongoDB para historial: {e}")
            self._mongodb_client = None
            self._mongo_db = None
    
    def register(
        self, 
        name: str, 
        host: str, 
        port: int, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Registrar un nuevo servicio
        
        Args:
            name: Nombre del servicio
            host: Host del servicio
            port: Puerto del servicio
            metadata: Información adicional del servicio
        """
        service_info = {
            "name": name,
            "host": host,
            "port": port,
            "status": "UNKNOWN",
            "last_check": None,
            "last_heartbeat": datetime.utcnow(),
            "registered_at": datetime.utcnow(),
            "failure_count": 0,
            "consecutive_failures": 0,
            "total_checks": 0,
            "successful_checks": 0,
            "metadata": metadata or {}
        }
        
        self._services[name] = service_info
        print(f"✅ Servicio registrado: {name} ({host}:{port})")
        
        # Realizar health check inicial
        self.health_check(name)
    
    def get(self, name: str) -> Dict[str, Any]:
        """
        Obtener información de un servicio
        
        Args:
            name: Nombre del servicio
        
        Returns:
            Información del servicio
        
        Raises:
            KeyError: Si el servicio no existe
        """
        if name not in self._services:
            raise KeyError(f"Servicio '{name}' no encontrado")
        return self._services[name].copy()
    
    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtener todos los servicios registrados
        
        Returns:
            Diccionario con todos los servicios
        """
        return {name: service.copy() for name, service in self._services.items()}
    
    def heartbeat(self, name: str) -> None:
        """
        Actualizar heartbeat de un servicio
        
        Args:
            name: Nombre del servicio
        """
        if name in self._services:
            self._services[name]["last_heartbeat"] = datetime.utcnow()
    
    def health_check(self, name: str) -> bool:
        """
        Realizar health check de un servicio
        
        Args:
            name: Nombre del servicio
        
        Returns:
            True si el servicio está UP, False en caso contrario
        """
        if name not in self._services:
            return False
        
        service = self._services[name]
        start_time = time.time()
        
        try:
            # Intentar conexión TCP al servicio
            with socket.create_connection(
                (service["host"], service["port"]), 
                timeout=5
            ) as sock:
                sock.close()
            
            # Calcular tiempo de respuesta
            response_time_ms = (time.time() - start_time) * 1000
            
            # Actualizar estado
            previous_status = service["status"]
            service["status"] = "UP"
            service["last_check"] = datetime.utcnow()
            service["consecutive_failures"] = 0
            service["total_checks"] += 1
            service["successful_checks"] += 1
            
            # Registrar en historial
            self._save_health_check(
                service_name=name,
                status="UP",
                response_time_ms=response_time_ms
            )
            
            # Notificar si cambió de DOWN/DEGRADED a UP
            if previous_status in ["DOWN", "DEGRADED"] and self._notification_service:
                self._notify_service_recovered(name, previous_status)
            
            return True
            
        except (socket.timeout, socket.error, ConnectionRefusedError) as e:
            # Servicio no responde
            previous_status = service["status"]
            service["consecutive_failures"] += 1
            service["failure_count"] += 1
            service["total_checks"] += 1
            service["last_check"] = datetime.utcnow()
            
            # Determinar nuevo estado
            if service["consecutive_failures"] >= self.failure_threshold:
                service["status"] = "DOWN"
            elif service["consecutive_failures"] > 0:
                service["status"] = "DEGRADED"
            
            # Registrar en historial
            self._save_health_check(
                service_name=name,
                status=service["status"],
                error_message=str(e)
            )
            
            # Notificar si cambió de UP a DOWN/DEGRADED
            if previous_status == "UP" and service["status"] in ["DOWN", "DEGRADED"]:
                self._notify_service_down(name, service["status"], str(e))
            
            return False
    
    def health_check_all(self) -> Dict[str, bool]:
        """
        Realizar health check de todos los servicios
        
        Returns:
            Diccionario con resultados {nombre: is_healthy}
        """
        results = {}
        for service_name in self._services.keys():
            results[service_name] = self.health_check(service_name)
        return results
    
    def get_service_metrics(self, name: str, hours: int = 24) -> Dict[str, Any]:
        """
        Obtener métricas de un servicio de las últimas horas
        
        Args:
            name: Nombre del servicio
            hours: Horas hacia atrás para calcular métricas
        
        Returns:
            Diccionario con métricas
        """
        if name not in self._services:
            return {}
        
        service = self._services[name]
        
        # Calcular uptime percentage
        uptime_percentage = 0.0
        if service["total_checks"] > 0:
            uptime_percentage = (
                service["successful_checks"] / service["total_checks"]
            ) * 100
        
        # Obtener historial de MongoDB si está disponible
        recent_history = []
        if self._mongo_db:
            try:
                cutoff_time = datetime.utcnow() - timedelta(hours=hours)
                recent_history = list(
                    self._mongo_db.service_health_checks.find(
                        {
                            "service_name": name,
                            "timestamp": {"$gte": cutoff_time}
                        }
                    ).sort("timestamp", -1).limit(100)
                )
            except Exception as e:
                print(f"⚠️ Error al obtener historial: {e}")
        
        return {
            "service_name": name,
            "current_status": service["status"],
            "uptime_percentage": round(uptime_percentage, 2),
            "total_checks": service["total_checks"],
            "successful_checks": service["successful_checks"],
            "failed_checks": service["failure_count"],
            "consecutive_failures": service["consecutive_failures"],
            "last_check": service["last_check"],
            "registered_at": service["registered_at"],
            "recent_history_count": len(recent_history)
        }
    
    def get_all_metrics(self, hours: int = 24) -> List[Dict[str, Any]]:
        """
        Obtener métricas de todos los servicios
        
        Args:
            hours: Horas hacia atrás para calcular métricas
        
        Returns:
            Lista de métricas de todos los servicios
        """
        return [
            self.get_service_metrics(name, hours)
            for name in self._services.keys()
        ]
    
    def get_service_history(
        self, 
        name: str, 
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Obtener historial de health checks de un servicio
        
        Args:
            name: Nombre del servicio
            limit: Número máximo de registros
        
        Returns:
            Lista de registros de health checks
        """
        if not self._mongo_db:
            return []
        
        try:
            history = list(
                self._mongo_db.service_health_checks.find(
                    {"service_name": name}
                ).sort("timestamp", -1).limit(limit)
            )
            
            # Convertir ObjectId a string
            for record in history:
                if "_id" in record:
                    record["_id"] = str(record["_id"])
            
            return history
        except Exception as e:
            print(f"⚠️ Error al obtener historial: {e}")
            return []
    
    def _save_health_check(
        self, 
        service_name: str, 
        status: str,
        response_time_ms: Optional[float] = None,
        error_message: Optional[str] = None
    ) -> None:
        """
        Guardar registro de health check en MongoDB
        
        Args:
            service_name: Nombre del servicio
            status: Estado del servicio (UP, DOWN, DEGRADED)
            response_time_ms: Tiempo de respuesta en milisegundos
            error_message: Mensaje de error si aplica
        """
        if self._mongo_db is None:
            return
        
        try:
            record = {
                "service_name": service_name,
                "status": status,
                "timestamp": datetime.utcnow(),
                "response_time_ms": response_time_ms,
                "error_message": error_message
            }
            
            self._mongo_db.service_health_checks.insert_one(record)
        except Exception as e:
            print(f"⚠️ Error al guardar health check: {e}")
    
    def _notify_service_down(
        self, 
        service_name: str, 
        status: str,
        error_message: Optional[str] = None
    ) -> None:
        """
        Notificar que un servicio cayó o está degradado
        
        Args:
            service_name: Nombre del servicio
            status: Estado del servicio (DOWN o DEGRADED)
            error_message: Mensaje de error
        """
        if not self._notification_service:
            return
        
        try:
            if status == "DOWN":
                self._notification_service.send_service_down_alert(
                    service_name=service_name,
                    error_message=error_message
                )
            elif status == "DEGRADED":
                self._notification_service.send_service_degraded_alert(
                    service_name=service_name,
                    reason=error_message
                )
        except Exception as e:
            print(f"⚠️ Error al enviar notificación: {e}")
    
    def _notify_service_recovered(
        self, 
        service_name: str,
        previous_status: str
    ) -> None:
        """
        Notificar que un servicio se recuperó
        
        Args:
            service_name: Nombre del servicio
            previous_status: Estado anterior del servicio
        """
        if not self._notification_service:
            return
        
        try:
            # Calcular tiempo de inactividad (aproximado)
            service = self._services[service_name]
            downtime_minutes = None
            
            if service.get("last_check"):
                delta = datetime.utcnow() - service["last_check"]
                downtime_minutes = delta.total_seconds() / 60
            
            self._notification_service.send_service_recovered_alert(
                service_name=service_name,
                downtime_minutes=downtime_minutes
            )
        except Exception as e:
            print(f"⚠️ Error al enviar notificación: {e}")


# Singleton
service_registry = ServiceRegistry()
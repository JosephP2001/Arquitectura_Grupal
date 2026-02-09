"""
Rutas de API para Dashboards de Monitoreo
- Service Registry Dashboard
- Circuit Breaker Dashboard
"""
from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import Dict, Any, List
import json
import asyncio
from datetime import datetime

# Importar servicios
from src.infrastructure.registry.service_registry import service_registry
from src.infrastructure.resilience.circuit_breaker import get_all_circuit_breakers

router = APIRouter()

# ============================================================================
# SERVICE REGISTRY DASHBOARD
# ============================================================================

@router.get("/registry/services")
async def get_all_services() -> Dict[str, Any]:
    """
    Obtener todos los servicios registrados con su estado actual
    
    Returns:
        Diccionario con información de todos los servicios
    """
    try:
        services = service_registry.get_all()
        
        # Convertir datetime a string para JSON
        for service_name, service_info in services.items():
            if service_info.get("last_check"):
                service_info["last_check"] = service_info["last_check"].isoformat()
            if service_info.get("last_heartbeat"):
                service_info["last_heartbeat"] = service_info["last_heartbeat"].isoformat()
            if service_info.get("registered_at"):
                service_info["registered_at"] = service_info["registered_at"].isoformat()
        
        return {
            "services": services,
            "total_services": len(services),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registry/services/{service_name}")
async def get_service_details(service_name: str) -> Dict[str, Any]:
    """
    Obtener detalles de un servicio específico
    
    Args:
        service_name: Nombre del servicio
    
    Returns:
        Información detallada del servicio
    """
    try:
        service = service_registry.get(service_name)
        
        # Convertir datetime a string
        if service.get("last_check"):
            service["last_check"] = service["last_check"].isoformat()
        if service.get("last_heartbeat"):
            service["last_heartbeat"] = service["last_heartbeat"].isoformat()
        if service.get("registered_at"):
            service["registered_at"] = service["registered_at"].isoformat()
        
        return service
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registry/services/{service_name}/metrics")
async def get_service_metrics(service_name: str, hours: int = 24) -> Dict[str, Any]:
    """
    Obtener métricas de un servicio
    
    Args:
        service_name: Nombre del servicio
        hours: Horas hacia atrás para calcular métricas (default: 24)
    
    Returns:
        Métricas del servicio
    """
    try:
        metrics = service_registry.get_service_metrics(service_name, hours)
        
        # Convertir datetime a string
        if metrics.get("last_check"):
            metrics["last_check"] = metrics["last_check"].isoformat()
        if metrics.get("registered_at"):
            metrics["registered_at"] = metrics["registered_at"].isoformat()
        
        return metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registry/services/{service_name}/history")
async def get_service_history(service_name: str, limit: int = 100) -> Dict[str, Any]:
    """
    Obtener historial de health checks de un servicio
    
    Args:
        service_name: Nombre del servicio
        limit: Número máximo de registros (default: 100)
    
    Returns:
        Historial de health checks
    """
    try:
        history = service_registry.get_service_history(service_name, limit)
        
        return {
            "service_name": service_name,
            "history": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/registry/metrics")
async def get_all_metrics(hours: int = 24) -> Dict[str, Any]:
    """
    Obtener métricas de todos los servicios
    
    Args:
        hours: Horas hacia atrás para calcular métricas (default: 24)
    
    Returns:
        Lista con métricas de todos los servicios
    """
    try:
        metrics = service_registry.get_all_metrics(hours)
        
        # Convertir datetime a string
        for metric in metrics:
            if metric.get("last_check"):
                metric["last_check"] = metric["last_check"].isoformat()
            if metric.get("registered_at"):
                metric["registered_at"] = metric["registered_at"].isoformat()
        
        return {
            "metrics": metrics,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/registry/health-check/{service_name}")
async def trigger_health_check(service_name: str) -> Dict[str, Any]:
    """
    Ejecutar health check manual de un servicio
    
    Args:
        service_name: Nombre del servicio
    
    Returns:
        Resultado del health check
    """
    try:
        is_healthy = service_registry.health_check(service_name)
        service = service_registry.get(service_name)
        
        return {
            "service_name": service_name,
            "is_healthy": is_healthy,
            "status": service["status"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Service '{service_name}' not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/registry/health-check")
async def trigger_all_health_checks() -> Dict[str, Any]:
    """
    Ejecutar health check de todos los servicios
    
    Returns:
        Resultados de health checks
    """
    try:
        results = service_registry.health_check_all()
        
        return {
            "results": results,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# CIRCUIT BREAKER DASHBOARD
# ============================================================================

@router.get("/circuit-breakers")
async def get_all_circuit_breakers_status() -> Dict[str, Any]:
    """
    Obtener estado de todos los circuit breakers
    
    Returns:
        Estado de todos los circuit breakers
    """
    try:
        breakers = get_all_circuit_breakers()
        
        statuses = {}
        for name, breaker in breakers.items():
            statuses[name] = breaker.get_status()
        
        return {
            "circuit_breakers": statuses,
            "total_breakers": len(statuses),
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/circuit-breakers/{breaker_name}")
async def get_circuit_breaker_status(breaker_name: str) -> Dict[str, Any]:
    """
    Obtener estado de un circuit breaker específico
    
    Args:
        breaker_name: Nombre del circuit breaker
    
    Returns:
        Estado del circuit breaker
    """
    try:
        breakers = get_all_circuit_breakers()
        
        if breaker_name not in breakers:
            raise HTTPException(
                status_code=404,
                detail=f"Circuit breaker '{breaker_name}' not found"
            )
        
        return breakers[breaker_name].get_status()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/circuit-breakers/{breaker_name}/metrics")
async def get_circuit_breaker_metrics(breaker_name: str) -> Dict[str, Any]:
    """
    Obtener métricas detalladas de un circuit breaker
    
    Args:
        breaker_name: Nombre del circuit breaker
    
    Returns:
        Métricas del circuit breaker
    """
    try:
        breakers = get_all_circuit_breakers()
        
        if breaker_name not in breakers:
            raise HTTPException(
                status_code=404,
                detail=f"Circuit breaker '{breaker_name}' not found"
            )
        
        breaker = breakers[breaker_name]
        status = breaker.get_status()
        
        # Obtener llamadas recientes
        recent_calls = breaker.metrics.get_recent_calls(limit=50)
        
        # Obtener historial de estados
        state_history = breaker.metrics.get_state_history()
        
        return {
            "name": breaker_name,
            "current_state": status["state"],
            "metrics": status["metrics"],
            "recent_calls": recent_calls,
            "state_history": state_history,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/circuit-breakers/{breaker_name}/reset")
async def reset_circuit_breaker(breaker_name: str) -> Dict[str, Any]:
    """
    Resetear un circuit breaker
    
    Args:
        breaker_name: Nombre del circuit breaker
    
    Returns:
        Confirmación de reset
    """
    try:
        breakers = get_all_circuit_breakers()
        
        if breaker_name not in breakers:
            raise HTTPException(
                status_code=404,
                detail=f"Circuit breaker '{breaker_name}' not found"
            )
        
        breakers[breaker_name].reset()
        
        return {
            "message": f"Circuit breaker '{breaker_name}' reset successfully",
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# WEBSOCKET para actualizaciones en tiempo real
# ============================================================================

class ConnectionManager:
    """Gestor de conexiones WebSocket"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass


manager = ConnectionManager()


@router.websocket("/ws/monitoring")
async def websocket_monitoring(websocket: WebSocket):
    """
    WebSocket para streaming de datos de monitoreo en tiempo real
    """
    await manager.connect(websocket)
    
    try:
        while True:
            # Enviar estado actual cada 2 segundos
            await asyncio.sleep(2)
            
            # Obtener estado de servicios
            services = service_registry.get_all()
            
            # Obtener estado de circuit breakers
            breakers = get_all_circuit_breakers()
            breaker_statuses = {
                name: breaker.get_status()
                for name, breaker in breakers.items()
            }
            
            # Preparar datos
            data = {
                "type": "monitoring_update",
                "timestamp": datetime.utcnow().isoformat(),
                "services": {
                    name: {
                        "status": service["status"],
                        "last_check": service.get("last_check").isoformat() if service.get("last_check") else None
                    }
                    for name, service in services.items()
                },
                "circuit_breakers": {
                    name: {
                        "state": status["state"],
                        "failure_count": status["failure_count"],
                        "metrics": status["metrics"]
                    }
                    for name, status in breaker_statuses.items()
                }
            }
            
            await websocket.send_text(json.dumps(data))
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
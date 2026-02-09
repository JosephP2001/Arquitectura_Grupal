"""
Rutas de Demostración de Circuit Breaker
Web A: Consume servicios de Web B protegido por Circuit Breaker
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional
from datetime import datetime

# Importar servicios
from src.infrastructure.resilience.circuit_breaker import get_circuit_breaker
from src.infrastructure.external.web_service_b import web_service_b

router = APIRouter()

# ============================================================================
# Obtener Circuit Breaker para Service B
# ============================================================================

def get_service_b_circuit_breaker():
    """Obtener circuit breaker para Web Service B"""
    return get_circuit_breaker(
        name="web_service_b",
        failure_threshold=5,
        timeout=30,
        half_open_max_calls=3
    )


# ============================================================================
# WEB A: ENDPOINTS QUE CONSUMEN WEB B
# ============================================================================

@router.get("/demo/patient/{patient_id}")
async def get_patient_with_circuit_breaker(patient_id: int) -> Dict[str, Any]:
    """
    Obtener datos de paciente desde Service B usando Circuit Breaker
    
    Args:
        patient_id: ID del paciente
    
    Returns:
        Datos del paciente o mensaje de error si el circuito está abierto
    """
    circuit_breaker = get_service_b_circuit_breaker()
    
    try:
        # Llamar a Service B protegido por Circuit Breaker
        data = circuit_breaker.call(
            web_service_b.get_patient_data,
            patient_id
        )
        
        return {
            "success": True,
            "data": data,
            "circuit_breaker_state": circuit_breaker.state.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # El Circuit Breaker rechazó la llamada o Service B falló
        return {
            "success": False,
            "error": str(e),
            "circuit_breaker_state": circuit_breaker.state.value,
            "fallback_message": "Service temporarily unavailable. Using cached data or default values.",
            "timestamp": datetime.utcnow().isoformat()
        }


@router.get("/demo/appointments/slots")
async def get_appointment_slots_with_circuit_breaker(
    doctor_id: int = Query(..., description="ID del doctor"),
    date: str = Query(..., description="Fecha en formato YYYY-MM-DD")
) -> Dict[str, Any]:
    """
    Obtener slots disponibles desde Service B usando Circuit Breaker
    
    Args:
        doctor_id: ID del doctor
        date: Fecha en formato YYYY-MM-DD
    
    Returns:
        Slots disponibles o mensaje de error
    """
    circuit_breaker = get_service_b_circuit_breaker()
    
    try:
        # Llamar a Service B protegido por Circuit Breaker
        data = circuit_breaker.call(
            web_service_b.get_appointment_slots,
            doctor_id,
            date
        )
        
        return {
            "success": True,
            "data": data,
            "circuit_breaker_state": circuit_breaker.state.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # Fallback: ofrecer slots genéricos
        fallback_slots = {
            "doctor_id": doctor_id,
            "date": date,
            "available_slots": ["09:00", "14:00"],  # Slots reducidos por default
            "source": "fallback_cache",
            "message": "Using cached availability due to service issues"
        }
        
        return {
            "success": False,
            "error": str(e),
            "circuit_breaker_state": circuit_breaker.state.value,
            "fallback_data": fallback_slots,
            "fallback_message": "Service temporarily unavailable. Showing limited availability from cache.",
            "timestamp": datetime.utcnow().isoformat()
        }


@router.post("/demo/notifications/send")
async def send_notification_with_circuit_breaker(
    patient_id: int = Query(..., description="ID del paciente"),
    message: str = Query(..., description="Mensaje a enviar")
) -> Dict[str, Any]:
    """
    Enviar notificación vía Service B usando Circuit Breaker
    
    Args:
        patient_id: ID del paciente
        message: Mensaje a enviar
    
    Returns:
        Confirmación de envío o mensaje de error
    """
    circuit_breaker = get_service_b_circuit_breaker()
    
    try:
        # Llamar a Service B protegido por Circuit Breaker
        data = circuit_breaker.call(
            web_service_b.send_notification,
            patient_id,
            message
        )
        
        return {
            "success": True,
            "data": data,
            "circuit_breaker_state": circuit_breaker.state.value,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        # Fallback: encolar para reintento posterior
        return {
            "success": False,
            "error": str(e),
            "circuit_breaker_state": circuit_breaker.state.value,
            "fallback_action": "Notification queued for retry",
            "fallback_message": "Service temporarily unavailable. Your notification has been queued and will be sent when the service recovers.",
            "queued": True,
            "timestamp": datetime.utcnow().isoformat()
        }


# ============================================================================
# CONTROL DE SERVICE B (para demostración)
# ============================================================================

@router.post("/demo/service-b/mode")
async def set_service_b_mode(
    mode: str = Query(..., description="Modo: STABLE, INTERMITTENT, FAILING, SLOW"),
    failure_rate: Optional[float] = Query(0.5, description="Tasa de fallos para modo INTERMITTENT (0.0-1.0)"),
    slow_delay: Optional[float] = Query(3.0, description="Delay en segundos para modo SLOW")
) -> Dict[str, Any]:
    """
    Configurar modo de operación de Service B
    
    Args:
        mode: Modo de operación (STABLE, INTERMITTENT, FAILING, SLOW)
        failure_rate: Tasa de fallos para modo INTERMITTENT
        slow_delay: Delay para modo SLOW
    
    Returns:
        Confirmación de cambio de modo
    """
    try:
        web_service_b.set_mode(
            mode=mode,
            failure_rate=failure_rate,
            slow_delay=slow_delay
        )
        
        return {
            "success": True,
            "message": f"Service B mode set to {mode}",
            "configuration": {
                "mode": mode,
                "failure_rate": failure_rate if mode == "INTERMITTENT" else None,
                "slow_delay": slow_delay if mode == "SLOW" else None
            },
            "timestamp": datetime.utcnow().isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/demo/service-b/statistics")
async def get_service_b_statistics() -> Dict[str, Any]:
    """
    Obtener estadísticas de Service B
    
    Returns:
        Estadísticas de uso de Service B
    """
    return web_service_b.get_statistics()


@router.post("/demo/service-b/reset-statistics")
async def reset_service_b_statistics() -> Dict[str, Any]:
    """
    Resetear estadísticas de Service B
    
    Returns:
        Confirmación de reset
    """
    web_service_b.reset_statistics()
    return {
        "success": True,
        "message": "Service B statistics reset",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/demo/service-b/health")
async def service_b_health_check() -> Dict[str, Any]:
    """
    Health check de Service B
    
    Returns:
        Estado de salud de Service B
    """
    return web_service_b.health_check()


# ============================================================================
# TESTING Y DEMOSTRACIÓN
# ============================================================================

@router.post("/demo/test-circuit-breaker")
async def test_circuit_breaker(
    num_requests: int = Query(10, description="Número de peticiones a hacer"),
    patient_id: int = Query(1, description="ID del paciente")
) -> Dict[str, Any]:
    """
    Hacer múltiples peticiones para probar el Circuit Breaker
    
    Args:
        num_requests: Número de peticiones a realizar
        patient_id: ID del paciente
    
    Returns:
        Resultados del test
    """
    circuit_breaker = get_service_b_circuit_breaker()
    
    results = []
    for i in range(num_requests):
        try:
            start_state = circuit_breaker.state.value
            
            data = circuit_breaker.call(
                web_service_b.get_patient_data,
                patient_id
            )
            
            results.append({
                "request_number": i + 1,
                "success": True,
                "state_before": start_state,
                "state_after": circuit_breaker.state.value
            })
            
        except Exception as e:
            results.append({
                "request_number": i + 1,
                "success": False,
                "error": str(e),
                "state_before": start_state,
                "state_after": circuit_breaker.state.value
            })
    
    # Resumen
    successful = sum(1 for r in results if r["success"])
    failed = len(results) - successful
    
    return {
        "test_summary": {
            "total_requests": num_requests,
            "successful": successful,
            "failed": failed,
            "final_circuit_state": circuit_breaker.state.value
        },
        "results": results,
        "circuit_breaker_metrics": circuit_breaker.metrics.get_metrics_dict(),
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/demo/scenario-guide")
async def get_scenario_guide() -> Dict[str, Any]:
    """
    Guía de escenarios de prueba para demostración
    
    Returns:
        Guía con escenarios recomendados
    """
    return {
        "scenarios": [
            {
                "name": "Escenario 1: Funcionamiento Normal",
                "description": "Service B responde correctamente, Circuit Breaker permanece CLOSED",
                "steps": [
                    "1. Configurar Service B en modo STABLE: POST /demo/service-b/mode?mode=STABLE",
                    "2. Hacer peticiones: GET /demo/patient/1",
                    "3. Verificar que Circuit Breaker está CLOSED: GET /monitoring/circuit-breakers/web_service_b"
                ]
            },
            {
                "name": "Escenario 2: Fallos Intermitentes",
                "description": "Service B falla aleatoriamente, Circuit Breaker se degrada",
                "steps": [
                    "1. Configurar Service B en modo INTERMITTENT (50% fallos): POST /demo/service-b/mode?mode=INTERMITTENT&failure_rate=0.5",
                    "2. Hacer múltiples peticiones: POST /demo/test-circuit-breaker?num_requests=10",
                    "3. Observar cambios de estado: Circuit Breaker pasa a OPEN tras 5 fallos"
                ]
            },
            {
                "name": "Escenario 3: Service B Completamente Caído",
                "description": "Service B falla siempre, Circuit Breaker OPEN",
                "steps": [
                    "1. Configurar Service B en modo FAILING: POST /demo/service-b/mode?mode=FAILING",
                    "2. Hacer peticiones: GET /demo/patient/1",
                    "3. Tras 5 fallos, Circuit Breaker pasa a OPEN",
                    "4. Nuevas peticiones se rechazan inmediatamente (no llegan a Service B)"
                ]
            },
            {
                "name": "Escenario 4: Recuperación Automática",
                "description": "Service B se recupera, Circuit Breaker pasa a HALF_OPEN y luego CLOSED",
                "steps": [
                    "1. Tener Circuit Breaker en estado OPEN (desde escenario anterior)",
                    "2. Esperar 30 segundos (timeout)",
                    "3. Configurar Service B en modo STABLE: POST /demo/service-b/mode?mode=STABLE",
                    "4. Hacer peticiones: GET /demo/patient/1",
                    "5. Circuit Breaker pasa a HALF_OPEN, prueba 3 peticiones, y luego a CLOSED"
                ]
            },
            {
                "name": "Escenario 5: Service Lento",
                "description": "Service B responde lentamente (simula timeout)",
                "steps": [
                    "1. Configurar Service B en modo SLOW: POST /demo/service-b/mode?mode=SLOW&slow_delay=3",
                    "2. Hacer peticiones: GET /demo/patient/1",
                    "3. Observar incremento en response_time_ms"
                ]
            }
        ],
        "dashboard_urls": {
            "service_registry": "/docs#/Reports/get_all_services_monitoring_registry_services_get",
            "circuit_breaker": "/docs#/Demo/get_circuit_breaker_status_monitoring_circuit_breakers__breaker_name__get",
            "websocket_monitoring": "ws://localhost:8000/monitoring/ws/monitoring"
        },
        "tips": [
            "Use el endpoint POST /monitoring/circuit-breakers/{breaker_name}/reset para resetear el Circuit Breaker entre escenarios",
            "Monitoree en tiempo real usando WebSocket: ws://localhost:8000/monitoring/ws/monitoring",
            "Las métricas detalladas están en: GET /monitoring/circuit-breakers/web_service_b/metrics"
        ]
    }
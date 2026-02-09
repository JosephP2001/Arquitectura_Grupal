"""
Circuit Breaker Pattern con Métricas y Dashboard
Protección contra fallos en cascada
"""
import time
from datetime import datetime, timedelta
from enum import Enum
from typing import Callable, Any, Optional, Dict, List
from collections import deque
import threading


class CircuitState(str, Enum):
    """Estados del Circuit Breaker"""
    CLOSED = "CLOSED"      # Funcionamiento normal
    OPEN = "OPEN"          # Fallo detectado, rechaza peticiones
    HALF_OPEN = "HALF_OPEN"  # Probando recuperación


class CircuitBreakerMetrics:
    """Métricas del Circuit Breaker"""
    
    def __init__(self):
        self.total_calls = 0
        self.successful_calls = 0
        self.failed_calls = 0
        self.rejected_calls = 0
        self.last_state_change = datetime.utcnow()
        self.state_history: deque = deque(maxlen=100)
        self.call_history: deque = deque(maxlen=1000)
        
        # Métricas de tiempo
        self.total_response_time = 0.0
        self.max_response_time = 0.0
        self.min_response_time = float('inf')
    
    def record_success(self, response_time: float):
        """Registrar llamada exitosa"""
        self.total_calls += 1
        self.successful_calls += 1
        self._update_response_time(response_time)
        self._record_call("SUCCESS", response_time)
    
    def record_failure(self, response_time: float = 0.0, error: str = ""):
        """Registrar llamada fallida"""
        self.total_calls += 1
        self.failed_calls += 1
        self._update_response_time(response_time)
        self._record_call("FAILURE", response_time, error)
    
    def record_rejection(self):
        """Registrar llamada rechazada (circuit OPEN)"""
        self.rejected_calls += 1
        self._record_call("REJECTED", 0.0)
    
    def record_state_change(self, old_state: CircuitState, new_state: CircuitState):
        """Registrar cambio de estado"""
        self.last_state_change = datetime.utcnow()
        self.state_history.append({
            "timestamp": self.last_state_change,
            "old_state": old_state.value,
            "new_state": new_state.value
        })
    
    def _update_response_time(self, response_time: float):
        """Actualizar métricas de tiempo de respuesta"""
        self.total_response_time += response_time
        self.max_response_time = max(self.max_response_time, response_time)
        self.min_response_time = min(self.min_response_time, response_time)
    
    def _record_call(self, result: str, response_time: float, error: str = ""):
        """Registrar llamada en historial"""
        self.call_history.append({
            "timestamp": datetime.utcnow(),
            "result": result,
            "response_time": response_time,
            "error": error
        })
    
    def get_average_response_time(self) -> float:
        """Obtener tiempo de respuesta promedio"""
        if self.successful_calls == 0:
            return 0.0
        return self.total_response_time / self.successful_calls
    
    def get_failure_rate(self) -> float:
        """Obtener tasa de fallos (%)"""
        if self.total_calls == 0:
            return 0.0
        return (self.failed_calls / self.total_calls) * 100
    
    def get_success_rate(self) -> float:
        """Obtener tasa de éxito (%)"""
        if self.total_calls == 0:
            return 0.0
        return (self.successful_calls / self.total_calls) * 100
    
    def get_metrics_dict(self) -> Dict[str, Any]:
        """Obtener todas las métricas como diccionario"""
        return {
            "total_calls": self.total_calls,
            "successful_calls": self.successful_calls,
            "failed_calls": self.failed_calls,
            "rejected_calls": self.rejected_calls,
            "success_rate": round(self.get_success_rate(), 2),
            "failure_rate": round(self.get_failure_rate(), 2),
            "average_response_time": round(self.get_average_response_time(), 3),
            "max_response_time": round(self.max_response_time, 3),
            "min_response_time": round(self.min_response_time, 3) if self.min_response_time != float('inf') else 0.0,
            "last_state_change": self.last_state_change.isoformat() if self.last_state_change else None
        }
    
    def get_recent_calls(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Obtener llamadas recientes"""
        recent = list(self.call_history)[-limit:]
        # Convertir datetime a string
        for call in recent:
            if "timestamp" in call:
                call["timestamp"] = call["timestamp"].isoformat()
        return recent
    
    def get_state_history(self) -> List[Dict[str, Any]]:
        """Obtener historial de cambios de estado"""
        history = list(self.state_history)
        # Convertir datetime a string
        for record in history:
            if "timestamp" in record:
                record["timestamp"] = record["timestamp"].isoformat()
        return history


class CircuitBreaker:
    """
    Circuit Breaker para protección contra fallos en cascada
    
    Estados:
    - CLOSED: Funcionamiento normal, todas las peticiones pasan
    - OPEN: Fallo detectado, se rechazan peticiones inmediatamente
    - HALF_OPEN: Probando recuperación, permite algunas peticiones
    
    Args:
        failure_threshold: Número de fallos para abrir el circuito
        timeout: Tiempo en segundos en estado OPEN antes de probar recuperación
        half_open_max_calls: Número máximo de llamadas en HALF_OPEN
    """
    
    def __init__(
        self,
        name: str = "default",
        failure_threshold: int = 5,
        timeout: int = 30,
        half_open_max_calls: int = 3
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.half_open_max_calls = half_open_max_calls
        
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[datetime] = None
        self._half_open_calls = 0
        self._lock = threading.Lock()
        
        # Métricas
        self.metrics = CircuitBreakerMetrics()
        
        print(f"🔌 Circuit Breaker '{name}' inicializado")
        print(f"   - Failure threshold: {failure_threshold}")
        print(f"   - Timeout: {timeout}s")
        print(f"   - Half-open max calls: {half_open_max_calls}")
    
    @property
    def state(self) -> CircuitState:
        """Obtener estado actual del circuito"""
        return self._state
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """
        Ejecutar función protegida por Circuit Breaker
        
        Args:
            func: Función a ejecutar
            *args: Argumentos posicionales
            **kwargs: Argumentos nombrados
        
        Returns:
            Resultado de la función
        
        Raises:
            Exception: Si el circuito está OPEN o la función falla
        """
        with self._lock:
            # Verificar si debemos cambiar de OPEN a HALF_OPEN
            if self._state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self._transition_to_half_open()
                else:
                    # Rechazar llamada
                    self.metrics.record_rejection()
                    raise Exception(
                        f"Circuit breaker '{self.name}' is OPEN. "
                        f"Retry after {self.timeout}s."
                    )
            
            # Limitar llamadas en HALF_OPEN
            if self._state == CircuitState.HALF_OPEN:
                if self._half_open_calls >= self.half_open_max_calls:
                    self.metrics.record_rejection()
                    raise Exception(
                        f"Circuit breaker '{self.name}' is HALF_OPEN. "
                        f"Too many test calls."
                    )
                self._half_open_calls += 1
        
        # Ejecutar función
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            response_time = time.time() - start_time
            
            # Registrar éxito
            with self._lock:
                self._on_success()
                self.metrics.record_success(response_time)
            
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            
            # Registrar fallo
            with self._lock:
                self._on_failure()
                self.metrics.record_failure(response_time, str(e))
            
            raise
    
    def _should_attempt_reset(self) -> bool:
        """Verificar si es momento de intentar resetear el circuito"""
        if not self._last_failure_time:
            return True
        
        elapsed = (datetime.utcnow() - self._last_failure_time).total_seconds()
        return elapsed >= self.timeout
    
    def _on_success(self):
        """Manejar llamada exitosa"""
        if self._state == CircuitState.HALF_OPEN:
            # Si todas las llamadas de prueba fueron exitosas, cerrar el circuito
            if self._half_open_calls >= self.half_open_max_calls:
                self._transition_to_closed()
        
        # En CLOSED, resetear contador de fallos
        if self._state == CircuitState.CLOSED:
            self._failure_count = 0
    
    def _on_failure(self):
        """Manejar llamada fallida"""
        self._failure_count += 1
        self._last_failure_time = datetime.utcnow()
        
        if self._state == CircuitState.HALF_OPEN:
            # Fallo en HALF_OPEN -> volver a OPEN
            self._transition_to_open()
        elif self._state == CircuitState.CLOSED:
            # Verificar si alcanzamos el threshold
            if self._failure_count >= self.failure_threshold:
                self._transition_to_open()
    
    def _transition_to_open(self):
        """Transición a estado OPEN"""
        old_state = self._state
        self._state = CircuitState.OPEN
        self._half_open_calls = 0
        self.metrics.record_state_change(old_state, CircuitState.OPEN)
        print(f"🔴 Circuit Breaker '{self.name}': {old_state.value} → OPEN")
    
    def _transition_to_half_open(self):
        """Transición a estado HALF_OPEN"""
        old_state = self._state
        self._state = CircuitState.HALF_OPEN
        self._half_open_calls = 0
        self.metrics.record_state_change(old_state, CircuitState.HALF_OPEN)
        print(f"🟡 Circuit Breaker '{self.name}': {old_state.value} → HALF_OPEN")
    
    def _transition_to_closed(self):
        """Transición a estado CLOSED"""
        old_state = self._state
        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0
        self.metrics.record_state_change(old_state, CircuitState.CLOSED)
        print(f"🟢 Circuit Breaker '{self.name}': {old_state.value} → CLOSED")
    
    def force_open(self):
        """Forzar circuito a estado OPEN (para testing)"""
        with self._lock:
            self._transition_to_open()
    
    def force_close(self):
        """Forzar circuito a estado CLOSED (para testing)"""
        with self._lock:
            self._transition_to_closed()
    
    def reset(self):
        """Resetear el circuit breaker completamente"""
        with self._lock:
            old_state = self._state
            self._state = CircuitState.CLOSED
            self._failure_count = 0
            self._half_open_calls = 0
            self._last_failure_time = None
            
            # No resetear métricas, solo estado
            if old_state != CircuitState.CLOSED:
                self.metrics.record_state_change(old_state, CircuitState.CLOSED)
            
            print(f"♻️ Circuit Breaker '{self.name}' reseteado")
    
    def get_status(self) -> Dict[str, Any]:
        """
        Obtener estado actual del circuit breaker
        
        Returns:
            Diccionario con estado y métricas
        """
        return {
            "name": self.name,
            "state": self._state.value,
            "failure_count": self._failure_count,
            "failure_threshold": self.failure_threshold,
            "timeout": self.timeout,
            "half_open_calls": self._half_open_calls,
            "half_open_max_calls": self.half_open_max_calls,
            "last_failure_time": self._last_failure_time.isoformat() if self._last_failure_time else None,
            "metrics": self.metrics.get_metrics_dict()
        }


# Registry global de circuit breakers
_circuit_breakers: Dict[str, CircuitBreaker] = {}


def get_circuit_breaker(
    name: str,
    failure_threshold: int = 5,
    timeout: int = 30,
    half_open_max_calls: int = 3
) -> CircuitBreaker:
    """
    Obtener o crear un circuit breaker
    
    Args:
        name: Nombre del circuit breaker
        failure_threshold: Umbral de fallos
        timeout: Timeout en segundos
        half_open_max_calls: Llamadas máximas en HALF_OPEN
    
    Returns:
        Instancia de CircuitBreaker
    """
    if name not in _circuit_breakers:
        _circuit_breakers[name] = CircuitBreaker(
            name=name,
            failure_threshold=failure_threshold,
            timeout=timeout,
            half_open_max_calls=half_open_max_calls
        )
    return _circuit_breakers[name]


def get_all_circuit_breakers() -> Dict[str, CircuitBreaker]:
    """Obtener todos los circuit breakers registrados"""
    return _circuit_breakers.copy()
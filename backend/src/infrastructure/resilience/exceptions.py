class CircuitBreakerOpen(Exception):
    """
    Se lanza cuando un Circuit Breaker está en estado OPEN
    y el servicio protegido no puede ser utilizado.
    """
    pass


class ServiceUnavailable(Exception):
    """
    Se lanza cuando un servicio requerido no está disponible
    en el Service Registry.
    """
    pass

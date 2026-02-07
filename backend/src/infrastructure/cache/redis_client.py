import redis
from src.infrastructure.registry.service_registry import service_registry


# --------------------------------------------------
# Redis Client Initialization
# --------------------------------------------------
_redis_client = None

def _init_redis():
    """Inicialización lazy para Redis, consulta al Service Registry"""
    global _redis_client
    
    if _redis_client is not None:
        return
    
    # Obtenemos los detalles de Redis del Service Registry
    redis_srv = service_registry.get("redis")
    
    if not redis_srv:
        raise RuntimeError("❌ Redis service not registered in Service Registry")

    # Creamos el cliente Redis
    _redis_client = redis.Redis(
        host=redis_srv["host"],
        port=redis_srv["port"],
        decode_responses=True
    )


# --------------------------------------------------
# Dependency: Obtenemos el cliente Redis
# --------------------------------------------------
def get_redis_client():
    """Dependency para obtener el cliente Redis"""
    if _redis_client is None:
        _init_redis()
    return _redis_client

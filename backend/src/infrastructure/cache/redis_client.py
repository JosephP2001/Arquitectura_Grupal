import redis
from src.infrastructure.registry.service_registry import service_registry
import os


_redis_client = None


def get_redis_client():
    """Obtiene cliente Redis usando Service Registry"""
    global _redis_client
    
    if _redis_client is not None:
        return _redis_client
    
    try:
        redis_service = service_registry.get("redis")
        host = redis_service["host"]
        port = redis_service["port"]
    except:
        host = os.getenv("REDIS_HOST", "localhost")
        port = int(os.getenv("REDIS_PORT", 6379))
    
    _redis_client = redis.Redis(
        host=host,
        port=port,
        db=0,
        decode_responses=True,
        socket_connect_timeout=5,
        socket_timeout=5
    )
    
    return _redis_client
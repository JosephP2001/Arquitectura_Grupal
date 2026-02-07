import redis

from src.infrastructure.registry.service_registry import service_registry


# --------------------------------------------------
# Redis (via Service Registry)
# --------------------------------------------------
redis_srv = service_registry.get("redis")

if not redis_srv:
    raise RuntimeError("❌ Redis service not registered in Service Registry")

_redis_client = redis.Redis(
    host=redis_srv["host"],
    port=redis_srv["port"],
    decode_responses=True,
)


# --------------------------------------------------
# Dependency
# --------------------------------------------------
def get_redis_client():
    """Dependency para obtener cliente Redis"""
    return _redis_client

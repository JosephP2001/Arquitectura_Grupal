import redis

_redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

def get_redis_client():
    return _redis_client

import redis  # type: ignore[import]
from redis import Redis

from app.config import settings

pool = redis.ConnectionPool(
    host=settings.REDIS_SERVER,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

r_cache = redis.Redis(connection_pool=pool)


def delete_cache_values(key_list: str, cache: Redis):
    while value := cache.rpop(key_list):
        cache.delete(value)

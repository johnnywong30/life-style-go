from app.data.redis.config import REDIS_HOST, REDIS_PORT
from app.data.redis.client import RedisClient


def getRedisConnection() -> RedisClient:
    r = RedisClient(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return r

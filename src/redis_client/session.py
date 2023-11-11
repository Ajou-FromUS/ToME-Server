from core.config import settings
import redis

REDIS_HOST = settings.REDIS_HOST
REDIS_PORT = settings.REDIS_PORT

RedisClient = redis.Redis(host=REDIS_HOST,port=REDIS_PORT,decode_responses=True)
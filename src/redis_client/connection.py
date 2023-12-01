from redis_client.session import RedisClient

import logging

logger = logging.getLogger()

def get_redis_client():
    redis_client = RedisClient
    try:
        # DB 연결 성공한 경우, DB 세션 시작
        logger.info("Redis Connected")
        yield redis_client
    finally:
        # DB 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.
        redis_client.quit()
        logger.info("Redis Disconnected")
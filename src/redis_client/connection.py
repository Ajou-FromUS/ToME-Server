from redis_client.session import RedisClient


def get_redis_client():
    redis_client = RedisClient
    try:
        # DB 연결 성공한 경우, DB 세션 시작
        yield redis_client
    finally:
        # DB 세션이 시작된 후, API 호출이 마무리되면 DB 세션을 닫아준다.
        redis_client.quit()
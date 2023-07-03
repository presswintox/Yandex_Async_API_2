import time

from redis import Redis

from tests.functional.settings import TestSettings

if __name__ == '__main__':
    redis_client = Redis(host=TestSettings.redis_host, port=6379)
    while True:
        if redis_client.ping():
            break
        time.sleep(1)

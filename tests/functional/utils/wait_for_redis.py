import backoff
from redis import Redis, ConnectionError, TimeoutError


@backoff.on_exception(backoff.expo, (ConnectionError, TimeoutError))
def waiter():
    print('Waiting for Redis')
    redis_client = Redis(host='redis', port=6379)
    redis_client.ping()


if __name__ == '__main__':
    waiter()

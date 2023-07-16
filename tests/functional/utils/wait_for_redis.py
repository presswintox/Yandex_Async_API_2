import time

from redis import Redis

if __name__ == '__main__':
    redis_client = Redis(host='redis', port=6379)
    while True:
        if redis_client.ping():
            break
        print('Waiting for Redis...')
        time.sleep(1)

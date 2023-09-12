import time
import os
import redis

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)
if __name__ == '__main__':
    while True:
        try:
            redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            print('Redis is up!')
            break
        except redis.ConnectionError:
            time.sleep(0.1)

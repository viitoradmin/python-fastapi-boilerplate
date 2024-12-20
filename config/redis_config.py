import os

import redis

from core.utils import constant_variable

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_BROKER_URL = os.environ.get('REDIS_BROKER_URL')



redis_client = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    decode_responses=constant_variable.STATUS_TRUE,
)

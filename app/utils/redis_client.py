import redis
from flask import current_app, json

from app.models.product import ProductModel

_redis_client = None

def init_redis(app):
    global _redis_client
    _redis_client = redis.Redis.from_url(app.config['REDIS_URL'])

def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.Redis.from_url(current_app.config['REDIS_URL'])
    return _redis_client

def add(redis_client, cache_key, list):
        redis_client.setex(cache_key, 3600, json.dumps(list))

def find_or_add(redis_client, cache_key, list):
    cached = redis_client.get(cache_key)

    if cached:
        data = json.loads(cached) 
    else:
        data = list
        add(redis_client, cache_key, data)

    return data

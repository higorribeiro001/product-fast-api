from app.models.product import ProductModel
from app.utils.redis_client import add, get_redis


def updating_list_products():
    redis_client = get_redis()
    cache_key = "products:list"
    add(redis_client, cache_key, [product.json() for product in ProductModel.query.all()])
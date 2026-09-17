import json
from redis import Redis

class RedisCachedBackend:
    def __init__(self, cache_ttl_seconds: int):
        self.redis = Redis(
            host="cache",
            port=6379,
            db=0,
            decode_responses=True
        )
        self.cache_ttl_seconds = cache_ttl_seconds

    def get_cache(self, key: str) -> dict:
        value = self.redis.get(key)
        if value is not None:
            return json.loads(value)

    def set_cache(self, key: str, value) -> None:
        self.redis.set(key, json.dumps(value), ex=self.cache_ttl_seconds)

    def delete_cache(self, key: str):
        self.redis.delete(key)
import json
from redis import Redis

class RedisCachedBackend:
    def __init__(self):
        self.redis = Redis(
            host="localhost",
            port=6378,
            db=0,
            decode_responses=True
        )

    def get_cache(self, key: str):
        return self.redis.get(json.loads(key))

    def set_cache(self, key: str, value) -> None:
        self.redis.set(key, json.dumps(value), ex=3600)

    def delete_cache(self, key: str):
        self.redis.delete(key)
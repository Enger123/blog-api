# import json
#
# from redis import Redis
#
# class RedisCached:
#     def __init__(self, ttl_seconds=3600):
#         self.redis = Redis(host="localhost", port=53605, decode_responses=True)
#         self.ttl_seconds = ttl_seconds
#
#     def set(self, key, value):
#         self.redis.set(key, json.dumps(value), ex=self.ttl_seconds)
#
#     def get(self, key):
#         return self.redis.get(key)
#
#     def delete(self, key):
#         self.redis.delete(key)
from cache.redis_caching import RedisCachedBackend

cache = RedisCachedBackend(cache_ttl_seconds=3600)

def test_set_cache():
    cache.set_cache("test_key", {'name': 'Roman'})
    res = cache.get_cache("test_key")
    assert res == {'name': 'Roman'}

def test_delete_cache():
    res = cache.delete_cache("test_key")
    assert res is None

def test_not_existing_key():
    res = cache.get_cache("unexisting_key")
    assert res is None
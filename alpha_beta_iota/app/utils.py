import json
from django.core.cache import cache

def cached(cache_key, timeout, fn):
    cached = cache.get(cache_key)
    miss = cached is None

    if cached:
        value = json.loads(cached)
    else:
        value = fn()
        cache.set(cache_key, json.dumps(value), timeout)

    return value, miss

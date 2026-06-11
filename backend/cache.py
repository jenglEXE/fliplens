import time

_cache = {}
CACHE_EXPIRY = 3600


def _normalize_key(query: str, filters: dict) -> str:
    filter_str = '&'.join(f'{k}={v}' for k, v in sorted(filters.items()) if v)
    return f'{query.lower().strip()}|{filter_str}'


def get_cached(query: str, filters: dict = {}):
    key = _normalize_key(query, filters)
    if key in _cache:
        result, timestamp = _cache[key]
        if time.time() - timestamp < CACHE_EXPIRY:
            return result
        del _cache[key]
    return None


def set_cached(query: str, filters: dict, value):
    key = _normalize_key(query, filters)
    _cache[key] = (value, time.time())


def clear_expired():
    now = time.time()
    expired = [k for k, (_, timestamp) in _cache.items()
               if now - timestamp >= CACHE_EXPIRY]
    for k in expired:
        del _cache[k]


def cache_size() -> int:
    return len(_cache)
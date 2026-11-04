import json
import inspect
import logging
from typing import Any, Optional, Callable
from functools import wraps
from redis import Redis

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

_SIMPLE_TYPES = (str, int, float, bool, type(None))


def serialize_value(value: Any) -> str:
    return json.dumps(value, default=str)


def deserialize_value(value: str) -> Any:
    return json.loads(value)


def build_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Build a cache key from a prefix and simple-typed arguments.

    Only positional/keyword args of basic types (str, int, float, bool, None)
    are included — complex objects like SQLAlchemy sessions are skipped.

    Examples:
        build_cache_key("product", 123)             -> "product:123"
        build_cache_key("products", page=1, limit=10) -> "products:limit:10:page:1"
    """
    parts = [prefix]
    for arg in args:
        if isinstance(arg, _SIMPLE_TYPES):
            parts.append(str(arg))
    for key, value in sorted(kwargs.items()):
        if isinstance(value, _SIMPLE_TYPES):
            parts.append(f"{key}:{value}")
    return ":".join(parts)


def get_from_cache(redis_client: Redis, key: str, deserialize: bool = True) -> Optional[Any]:
    if not redis_client or not settings.redis_enabled:
        return None
    try:
        value = redis_client.get(key)
        if value is None:
            logger.debug(f"Cache miss: {key}")
            return None
        logger.debug(f"Cache hit: {key}")
        return deserialize_value(value) if deserialize else value
    except Exception as e:
        logger.error(f"Redis GET error for key {key}: {e}")
        return None


def set_to_cache(
    redis_client: Redis,
    key: str,
    value: Any,
    ttl: int,
    serialize: bool = True,
) -> bool:
    if not redis_client or not settings.redis_enabled:
        return False
    try:
        cache_value = serialize_value(value) if serialize else value
        redis_client.setex(key, ttl, cache_value)
        logger.debug(f"Cache set: {key} (TTL: {ttl}s)")
        return True
    except Exception as e:
        logger.error(f"Redis SET error for key {key}: {e}")
        return False


def delete_from_cache(redis_client: Redis, key: str) -> bool:
    if not redis_client or not settings.redis_enabled:
        return False
    try:
        redis_client.delete(key)
        logger.debug(f"Cache deleted: {key}")
        return True
    except Exception as e:
        logger.error(f"Redis DELETE error for key {key}: {e}")
        return False


def invalidate_pattern(redis_client: Redis, pattern: str) -> int:
    """
    Delete all keys matching a Redis glob pattern.

    Example:
        invalidate_pattern(redis_client, "products:*")
    """
    if not redis_client or not settings.redis_enabled:
        return 0
    try:
        keys = list(redis_client.scan_iter(match=pattern))
        if keys:
            count = redis_client.delete(*keys)
            logger.info(f"Invalidated {count} keys matching: {pattern}")
            return count
        return 0
    except Exception as e:
        logger.error(f"Redis pattern invalidation error: {e}")
        return 0


def cache_result(redis_client: Redis, key_prefix: str, ttl: int):
    """
    Decorator that caches a function's return value in Redis.

    Usage:
        @cache_result(redis_client, "product", ttl=300)
        def get_product(product_id: int, db: Session = Depends(get_db_session)):
            ...

        @cache_result(redis_client, "products", ttl=60)
        async def list_products(skip: int = 0, limit: int = 10, db=Depends(...)):
            ...
    """
    def decorator(func: Callable):
        def _build_key(*args, **kwargs) -> str:
            return build_cache_key(key_prefix, *args, **kwargs)

        def _to_serializable(result: Any) -> Any:
            if hasattr(result, "model_dump"):
                return result.model_dump(mode="json")
            return result

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_key = _build_key(*args, **kwargs)
            cached = get_from_cache(redis_client, cache_key)
            if cached is not None:
                return cached
            result = func(*args, **kwargs)
            if result is not None:
                try:
                    set_to_cache(redis_client, cache_key, _to_serializable(result), ttl)
                except Exception as e:
                    logger.warning(f"Could not cache result for {cache_key}: {e}")
            return result

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_key = _build_key(*args, **kwargs)
            cached = get_from_cache(redis_client, cache_key)
            if cached is not None:
                return cached
            result = await func(*args, **kwargs)
            if result is not None:
                try:
                    set_to_cache(redis_client, cache_key, _to_serializable(result), ttl)
                except Exception as e:
                    logger.warning(f"Could not cache result for {cache_key}: {e}")
            return result

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator

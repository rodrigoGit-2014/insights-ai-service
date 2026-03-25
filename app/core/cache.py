import hashlib
import json
import logging
from typing import Optional, Any
import redis
from app.core.config import settings

logger = logging.getLogger(__name__)

class RedisCache:
    def __init__(self):
        try:
            self.client = redis.from_url(settings.REDIS_URL, socket_timeout=2)
            self.client.ping()
            self.available = True
            logger.info("Redis cache connected")
        except Exception:
            self.available = False
            logger.warning("Redis not available, running without cache")

    def get(self, key: str) -> Optional[Any]:
        if not self.available:
            return None
        try:
            data = self.client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None

    def set(self, key: str, value: Any, ttl: int = None) -> bool:
        if not self.available:
            return False
        try:
            ttl = ttl or settings.INSIGHT_CACHE_TTL_SECONDS
            self.client.setex(key, ttl, json.dumps(value, default=str))
            return True
        except Exception:
            return False

    def delete_pattern(self, pattern: str) -> int:
        if not self.available:
            return 0
        try:
            keys = list(self.client.scan_iter(match=pattern))
            if keys:
                return self.client.delete(*keys)
            return 0
        except Exception:
            return 0

cache = RedisCache()

def make_cache_key(prefix: str, **kwargs) -> str:
    sorted_params = json.dumps(kwargs, sort_keys=True, default=str)
    param_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:12]
    return f"v1:{prefix}:{param_hash}"

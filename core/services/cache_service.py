import hashlib
import json
import logging
from typing import Any, Callable, Optional, List
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)

class CacheService:
    """Advanced caching service with Redis backend"""
    
    DEFAULT_TTL = 3600  # 1 hour
    SHORT_TTL = 300     # 5 minutes
    LONG_TTL = 86400    # 24 hours
    
    # Cache key prefixes
    PREFIXES = {
        'user': 'usr',
        'post': 'pst',
        'category': 'cat',
        'api': 'api',
        'query': 'qry',
    }
    
    @classmethod
    def generate_key(cls, prefix: str, **kwargs) -> str:
        """Generate cache key from prefix and parameters"""
        if prefix not in cls.PREFIXES:
            raise ValueError(f"Invalid cache prefix: {prefix}")
        
        params_str = json.dumps(kwargs, sort_keys=True, default=str)
        hash_suffix = hashlib.md5(params_str.encode()).hexdigest()[:8]
        return f"{cls.PREFIXES[prefix]}:{hash_suffix}"
    
    @classmethod
    def get(cls, key: str, default=None) -> Any:
        """Get value from cache"""
        try:
            result = cache.get(key, default)
            if result != default:
                logger.debug(f"Cache HIT for key: {key}")
            else:
                logger.debug(f"Cache MISS for key: {key}")
            return result
        except Exception as e:
            logger.error(f"Cache GET failed for key {key}: {str(e)}")
            return default
    
    @classmethod
    def set(cls, key: str, value: Any, ttl: int = DEFAULT_TTL) -> bool:
        """Set value in cache"""
        try:
            cache.set(key, value, ttl)
            logger.debug(f"Cache SET for key: {key}, TTL: {ttl}")
            return True
        except Exception as e:
            logger.error(f"Cache SET failed for key {key}: {str(e)}")
            return False
    
    @classmethod
    def get_or_set(cls, key: str, callable_func: Callable, ttl: int = DEFAULT_TTL) -> Any:
        """Get from cache or set using callable"""
        result = cls.get(key)
        if result is None:
            try:
                result = callable_func()
                cls.set(key, result, ttl)
            except Exception as e:
                logger.error(f"Cache callable failed for key {key}: {str(e)}")
                return None
        return result
    
    @classmethod
    def delete(cls, key: str) -> bool:
        """Delete single cache key"""
        try:
            cache.delete(key)
            logger.debug(f"Cache DELETE for key: {key}")
            return True
        except Exception as e:
            logger.error(f"Cache DELETE failed for key {key}: {str(e)}")
            return False
    
    @classmethod
    def delete_pattern(cls, pattern: str) -> bool:
        """Delete cache keys matching pattern"""
        try:
            cache.delete_pattern(f"*{pattern}*")
            logger.info(f"Cache DELETE PATTERN: {pattern}")
            return True
        except Exception as e:
            logger.error(f"Cache DELETE PATTERN failed for {pattern}: {str(e)}")
            return False
    
    @classmethod
    def invalidate_user_cache(cls, user_id: str):
        """Invalidate all user-related cache"""
        patterns = [
            f"usr:*{user_id}*",
            "api:users*",
            "qry:user*"
        ]
        for pattern in patterns:
            cls.delete_pattern(pattern)
    
    @classmethod
    def invalidate_post_cache(cls, post_id: str = None):
        """Invalidate post-related cache"""
        patterns = [
            "api:posts*",
            "qry:post*"
        ]
        if post_id:
            patterns.append(f"pst:*{post_id}*")
        
        for pattern in patterns:
            cls.delete_pattern(pattern)
    
    @classmethod
    def get_cache_stats(cls) -> dict:
        """Get cache statistics"""
        try:
            info = cache._cache.get_client().info()
            return {
                'used_memory': info.get('used_memory_human'),
                'connected_clients': info.get('connected_clients'),
                'total_commands_processed': info.get('total_commands_processed'),
                'keyspace_hits': info.get('keyspace_hits'),
                'keyspace_misses': info.get('keyspace_misses'),
                'hit_rate': round(
                    info.get('keyspace_hits', 0) / 
                    max(info.get('keyspace_hits', 0) + info.get('keyspace_misses', 0), 1) * 100, 2
                )
            }
        except Exception as e:
            logger.error(f"Failed to get cache stats: {str(e)}")
            return {}
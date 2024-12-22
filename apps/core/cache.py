from typing import Any, Optional
from django.core.cache import cache
from django.conf import settings
import hashlib
import json

class CacheManager:
    """
    缓存管理器
    """
    @staticmethod
    def _generate_key(prefix: str, identifier: Any) -> str:
        """
        生成缓存键
        """
        if isinstance(identifier, dict):
            # 对字典进行排序以确保相同内容生成相同的键
            identifier = json.dumps(identifier, sort_keys=True)
        
        key = f"{identifier}".encode('utf-8')
        hash_key = hashlib.md5(key).hexdigest()
        return f"{settings.CACHE_KEY_PREFIX}{prefix}:{hash_key}"

    @classmethod
    def get(cls, prefix: str, identifier: Any) -> Optional[Any]:
        """
        获取缓存数据
        """
        key = cls._generate_key(prefix, identifier)
        return cache.get(key)

    @classmethod
    def set(cls, prefix: str, identifier: Any, data: Any) -> None:
        """
        设置缓存数据
        """
        key = cls._generate_key(prefix, identifier)
        timeout = settings.CACHE_TTL.get(prefix, 3600)
        cache.set(key, data, timeout)

    @classmethod
    def delete(cls, prefix: str, identifier: Any) -> None:
        """
        删除缓存数据
        """
        key = cls._generate_key(prefix, identifier)
        cache.delete(key)

    @classmethod
    def clear_prefix(cls, prefix: str) -> None:
        """
        清除指定前缀的所有缓存
        """
        pattern = f"{settings.CACHE_KEY_PREFIX}{prefix}:*"
        keys = cache.keys(pattern)
        if keys:
            cache.delete_many(keys)
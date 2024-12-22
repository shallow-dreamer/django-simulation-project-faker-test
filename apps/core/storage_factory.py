from typing import Dict, Type
from apps.core.storage import BaseStorage, LocalStorage, S3Storage
from django.conf import settings

class StorageFactory:
    """
    存储服务工厂
    """
    _storage_types: Dict[str, Type[BaseStorage]] = {
        'local': LocalStorage,
        's3': S3Storage
    }
    
    _instance = None
    
    @classmethod
    def get_storage(cls) -> BaseStorage:
        """
        获取存储服务实例
        """
        if cls._instance is None:
            storage_type = getattr(settings, 'DEFAULT_STORAGE_TYPE', 'local')
            storage_class = cls._storage_types.get(storage_type)
            if not storage_class:
                raise ValueError(f"Unsupported storage type: {storage_type}")
            cls._instance = storage_class()
        return cls._instance 
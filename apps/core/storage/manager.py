from typing import Dict, Type
from django.conf import settings
from .base import BaseStorage
from .local import LocalStorage
from .s3 import S3Storage

class StorageManager:
    """
    存储管理器
    """
    _storages: Dict[str, Type[BaseStorage]] = {
        'local': LocalStorage,
        's3': S3Storage
    }
    
    _instances: Dict[str, BaseStorage] = {}
    
    @classmethod
    def get_storage(cls, storage_type: str = None) -> BaseStorage:
        """
        获取存储实例
        """
        if not storage_type:
            storage_type = settings.DEFAULT_STORAGE_TYPE
            
        if storage_type not in cls._instances:
            storage_class = cls._storages.get(storage_type)
            if not storage_class:
                raise ValueError(f"Unsupported storage type: {storage_type}")
                
            config = settings.STORAGE_CONFIG.get(storage_type, {})
            cls._instances[storage_type] = storage_class(config)
            
        return cls._instances[storage_type]

    @classmethod
    def register_storage(cls, name: str, storage_class: Type[BaseStorage]):
        """
        注册新的存储类型
        """
        cls._storages[name] = storage_class 
class StorageError(Exception):
    """
    存储异常
    """
    pass

class CacheError(Exception):
    """
    缓存异常
    """
    pass

class ValidationError(Exception):
    """
    验证异常
    """
    pass

class ServiceError(Exception):
    """
    服务异常
    """
    pass

class ConfigurationError(Exception):
    """
    配置异常
    """
    pass 
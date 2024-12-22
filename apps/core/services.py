from typing import Any, Dict, Optional
from django.db import transaction

class BaseService:
    """
    服务基类，提供通用的服务方法
    """
    
    @staticmethod
    def handle_transaction(func):
        """
        事务装饰器
        """
        def wrapper(*args, **kwargs):
            with transaction.atomic():
                return func(*args, **kwargs)
        return wrapper 
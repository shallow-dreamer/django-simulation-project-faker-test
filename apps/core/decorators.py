import time
import logging
from functools import wraps
from typing import Any, Callable

logger = logging.getLogger('performance')

def log_execution_time(func: Callable) -> Callable:
    """
    记录函数执行时间的装饰器
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        logger.info(
            f'Function: {func.__name__} | '
            f'Duration: {duration:.2f}s | '
            f'Args: {args} | '
            f'Kwargs: {kwargs}'
        )
        
        return result
    return wrapper

def monitor_memory(func: Callable) -> Callable:
    """
    监控内存使用的装饰器
    """
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        import psutil
        process = psutil.Process()
        memory_before = process.memory_info().rss
        
        result = func(*args, **kwargs)
        
        memory_after = process.memory_info().rss
        memory_diff = memory_after - memory_before
        
        logger.info(
            f'Function: {func.__name__} | '
            f'Memory diff: {memory_diff/1024/1024:.2f}MB'
        )
        
        return result
    return wrapper 
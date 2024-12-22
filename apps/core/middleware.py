import time
import logging
from typing import Any, Callable
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger('performance')

class PerformanceMonitorMiddleware:
    """
    性能监控中间件
    """
    def __init__(self, get_response: Callable):
        self.get_response = get_response
    
    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.time()
        
        response = self.get_response(request)
        
        duration = time.time() - start_time
        
        # 记录请求处理时间
        logger.info(
            f'Path: {request.path} | '
            f'Method: {request.method} | '
            f'Duration: {duration:.2f}s | '
            f'Status: {response.status_code}'
        )
        
        # 如果处理时间超过阈值，记录警告
        if duration > 1.0:  # 1秒
            logger.warning(
                f'Slow request detected - Path: {request.path} | '
                f'Duration: {duration:.2f}s'
            )
        
        return response 
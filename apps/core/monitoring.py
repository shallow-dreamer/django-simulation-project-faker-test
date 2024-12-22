from typing import Dict, Any
from celery.result import AsyncResult
import logging
import psutil
import redis
from django.conf import settings
from datetime import datetime, timedelta
from django.core.cache import cache
from django.db import connection

logger = logging.getLogger('performance')

class SystemMonitor:
    """
    系统监控服务
    """
    @classmethod
    def get_system_metrics(cls) -> Dict[str, Any]:
        """
        获取系统指标
        """
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        metrics = {
            'cpu_usage': cpu_percent,
            'memory_usage': memory.percent,
            'disk_usage': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            },
            'timestamp': datetime.now().isoformat()
        }
        
        logger.info(f'System metrics: {metrics}')
        return metrics

    @classmethod
    def get_redis_metrics(cls) -> Dict[str, Any]:
        """
        获取Redis指标
        """
        try:
            redis_client = redis.from_url(settings.CELERY_BROKER_URL)
            info = redis_client.info()
            
            metrics = {
                'connected_clients': info['connected_clients'],
                'used_memory': info['used_memory'],
                'used_memory_peak': info['used_memory_peak'],
                'total_commands_processed': info['total_commands_processed']
            }
            
            logger.info(f'Redis metrics: {metrics}')
            return metrics
        except Exception as e:
            logger.error(f'Failed to get Redis metrics: {e}')
            return {}

class DatabaseMonitor:
    """
    数据库监控服务
    """
    @classmethod
    def get_db_metrics(cls) -> Dict[str, Any]:
        """
        获取数据库指标
        """
        metrics = {
            'total_queries': len(connection.queries),
            'slow_queries': [
                q for q in connection.queries
                if float(q['time']) > 0.1  # 100ms
            ]
        }
        
        if metrics['slow_queries']:
            logger.warning(f'Slow queries detected: {metrics["slow_queries"]}')
        
        return metrics

class CacheMonitor:
    """
    缓存监控服务
    """
    @classmethod
    def get_cache_metrics(cls) -> Dict[str, Any]:
        """
        获取缓存指标
        """
        try:
            cache_client = cache.client.get_client()
            info = cache_client.info()
            
            metrics = {
                'hits': info.get('keyspace_hits', 0),
                'misses': info.get('keyspace_misses', 0),
                'keys': len(cache_client.keys('*')),
                'memory_used': info.get('used_memory', 0)
            }
            
            # 计算缓存命中率
            total = metrics['hits'] + metrics['misses']
            metrics['hit_rate'] = (metrics['hits'] / total * 100) if total > 0 else 0
            
            logger.info(f'Cache metrics: {metrics}')
            return metrics
        except Exception as e:
            logger.error(f'Failed to get cache metrics: {e}')
            return {}

class TaskMonitor:
    """
    Celery任务监控服务
    """
    
    @staticmethod
    def get_task_status(task_id: str) -> Dict[str, Any]:
        """
        获取任务状态
        """
        result = AsyncResult(task_id)
        return {
            'task_id': task_id,
            'status': result.status,
            'result': result.result if result.ready() else None
        }
    
    @staticmethod
    def revoke_task(task_id: str, terminate: bool = False) -> bool:
        """
        取消任务
        """
        try:
            AsyncResult(task_id).revoke(terminate=terminate)
            return True
        except Exception:
            return False 
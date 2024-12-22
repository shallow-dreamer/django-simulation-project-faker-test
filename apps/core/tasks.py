from celery import shared_task
from core.cache import CacheManager
from .monitoring import SystemMonitor, DatabaseMonitor, CacheMonitor
import logging

logger = logging.getLogger('performance')

@shared_task
def clear_expired_caches():
    """
    清理过期缓存
    """
    prefixes = ['parameter', 'simulation', 'file']
    for prefix in prefixes:
        CacheManager.clear_prefix(prefix)
    return "Cache cleanup completed"

@shared_task
def collect_system_metrics():
    """
    收集系统指标
    """
    try:
        metrics = {
            'system': SystemMonitor.get_system_metrics(),
            'redis': SystemMonitor.get_redis_metrics(),
            'database': DatabaseMonitor.get_db_metrics(),
            'cache': CacheMonitor.get_cache_metrics()
        }
        
        # 这里可以将指标保存到数据库或时序数据库中
        logger.info(f'Collected metrics: {metrics}')
        return metrics
    except Exception as e:
        logger.error(f'Failed to collect metrics: {e}')
        raise

@shared_task
def monitor_slow_operations():
    """
    监控慢操作
    """
    try:
        db_metrics = DatabaseMonitor.get_db_metrics()
        if db_metrics['slow_queries']:
            logger.warning(
                f'Found {len(db_metrics["slow_queries"])} slow queries'
            )
        
        # 检查缓存性能
        cache_metrics = CacheMonitor.get_cache_metrics()
        if cache_metrics.get('hit_rate', 0) < 50:
            logger.warning(
                f'Low cache hit rate: {cache_metrics["hit_rate"]}%'
            )
    except Exception as e:
        logger.error(f'Failed to monitor operations: {e}')
        raise
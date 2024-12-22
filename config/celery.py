import os
from celery import Celery

"""
Celery配置文件

设计考虑：
1. 配置Celery用于处理异步任务
2. 支持仿真计算等耗时操作的异步执行
3. 集成Django配置
4. 支持任务结果的持久化存储
"""

# 设置默认Django配置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# 创建Celery实例
app = Celery('config')

# 使用Django的配置文件配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    """
    调试任务
    用于测试Celery是否正常工作
    """
    print(f'Request: {self.request!r}') 
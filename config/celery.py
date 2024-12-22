import os
from celery import Celery

# 设置默认Django设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

app = Celery('django_simulation_project')

# 使用CELERY作为设置的前缀，在settings中进行配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动从已注册app中加载任务
app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}') 
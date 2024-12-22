from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from .models import ComSimulation, SimulationHistory

@shared_task
def cleanup_old_simulations():
    """
    清理旧的仿真记录
    """
    # 清理30天前的已完成仿真
    threshold = timezone.now() - timedelta(days=30)
    
    # 获取要清理的仿真
    old_simulations = ComSimulation.objects.filter(
        created_at__lt=threshold,
        status='completed'
    )
    
    # 记录清理操作
    for simulation in old_simulations:
        SimulationHistory.objects.create(
            simulation=simulation,
            status='cleaned',
            execution_time=0,
            error_message='Cleaned by automated task'
        )
    
    # 执行清理
    deleted_count = old_simulations.delete()[0]
    
    return f'Cleaned {deleted_count} old simulations' 
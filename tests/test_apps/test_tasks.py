import pytest
from datetime import timedelta
from django.utils import timezone
from apps.com_simulation.models import ComSimulation
from apps.com_simulation.tasks import cleanup_old_simulations

pytestmark = pytest.mark.django_db

class TestCleanupTask:
    def test_cleanup_old_simulations(self):
        # 创建一些旧的仿真记录
        old_date = timezone.now() - timedelta(days=31)
        
        old_simulation = ComSimulation.objects.create(
            name='Old Simulation',
            status='completed',
            configuration={'test': 'config'}
        )
        # 修改创建时间
        ComSimulation.objects.filter(id=old_simulation.id).update(created_at=old_date)
        
        # 创建新的仿真记录
        new_simulation = ComSimulation.objects.create(
            name='New Simulation',
            status='completed',
            configuration={'test': 'config'}
        )
        
        # 运行清理任务
        result = cleanup_old_simulations()
        
        # 验证结果
        assert 'Cleaned 1 old simulations' in result
        assert not ComSimulation.objects.filter(id=old_simulation.id).exists()
        assert ComSimulation.objects.filter(id=new_simulation.id).exists() 
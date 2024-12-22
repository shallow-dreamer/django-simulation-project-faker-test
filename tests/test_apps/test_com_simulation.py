import pytest
from unittest.mock import patch
from django.urls import reverse
from apps.com_simulation.models import ComSimulation
from apps.com_simulation.services import SimulationService
from apps.parameter_processing.models import SParameter

pytestmark = pytest.mark.django_db

class TestComSimulationAPI:
    def test_create_simulation(self, authenticated_client, uploaded_file):
        # 创建测试参数
        parameter = SParameter.objects.create(
            file=uploaded_file,
            frequency=1000.0,
            value={'test': 'data'}
        )
        
        url = reverse('comsimulation-list')
        data = {
            'name': 'Test Simulation',
            'parameters': [parameter.id],
            'configuration': {'test': 'config'}
        }
        
        response = authenticated_client.post(url, data, format='json')
        assert response.status_code == 201

    @patch('apps.com_simulation.services.run_simulation_task.delay')
    def test_run_simulation(self, mock_task, authenticated_client):
        simulation = ComSimulation.objects.create(
            name='Test Simulation',
            configuration={'test': 'config'},
            status='created'
        )
        
        url = reverse('comsimulation-run-simulation', kwargs={'pk': simulation.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == 200
        assert response.data['status'] == 'pending'
        mock_task.assert_called_once_with(simulation.id)

class TestSimulationService:
    def test_get_simulation_status(self):
        simulation = ComSimulation.objects.create(
            name='Test Simulation',
            configuration={'test': 'config'},
            status='completed',
            result={'test': 'result'}
        )
        
        service = SimulationService()
        status = service.get_simulation_status(simulation.id)
        
        assert status['status'] == 'completed'
        assert 'result' in status 
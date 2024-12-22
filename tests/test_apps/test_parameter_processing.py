import pytest
from django.urls import reverse
from apps.parameter_processing.models import SParameter
from apps.parameter_processing.services import ParameterProcessingService

pytestmark = pytest.mark.django_db

class TestParameterProcessingAPI:
    def test_process_parameter(self, authenticated_client, uploaded_file):
        # 创建测试参数
        parameter = SParameter.objects.create(
            file=uploaded_file,
            frequency=1000.0,
            value={'test': 'data'}
        )
        
        url = reverse('sparameter-process-parameter', kwargs={'pk': parameter.id})
        response = authenticated_client.post(url)
        
        assert response.status_code == 200
        assert response.data['status'] == 'success'

class TestParameterProcessingService:
    def test_process_parameter(self, uploaded_file):
        parameter = SParameter.objects.create(
            file=uploaded_file,
            frequency=1000.0,
            value={'test': 'data'}
        )
        
        service = ParameterProcessingService()
        result = service.process_parameter(parameter)
        
        assert result['status'] == 'success'
        assert 'data' in result 
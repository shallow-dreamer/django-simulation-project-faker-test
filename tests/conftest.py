import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.file_management.models import FileCollection, UploadedFile
from apps.parameter_processing.models import SParameter
from apps.com_simulation.models import ComSimulation

@pytest.fixture
def api_client():
    """
    提供API测试客户端
    用于模拟HTTP请求和响应
    """
    return APIClient()

@pytest.fixture
def test_user(db):
    """
    创建测试用户
    
    提供：
    1. 基本用户信息
    2. 测试权限设置
    3. 用户认证数据
    """
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        password='testpass123',
        email='test@example.com'
    )

@pytest.fixture
def authenticated_client(api_client, test_user):
    """
    提供已认证的测试客户端
    
    功能：
    1. 客户端带有认证信息
    2. 可直接访问需要认证的接口
    3. 模拟真实用户行为
    """
    api_client.force_authenticate(user=test_user)
    return api_client

@pytest.fixture
def file_collection(test_user):
    return FileCollection.objects.create(
        name='Test Collection',
        description='Test Description',
        user=test_user
    )

@pytest.fixture
def uploaded_file(file_collection):
    return UploadedFile.objects.create(
        file='test/test.txt',
        name='test.txt',
        file_type='text',
        collection=file_collection
    ) 
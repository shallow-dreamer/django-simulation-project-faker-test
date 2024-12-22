import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.file_management.models import FileCollection, UploadedFile
from apps.parameter_processing.models import SParameter
from apps.com_simulation.models import ComSimulation

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    User = get_user_model()
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )

@pytest.fixture
def authenticated_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client

@pytest.fixture
def file_collection(user):
    return FileCollection.objects.create(
        name='Test Collection',
        description='Test Description',
        user=user
    )

@pytest.fixture
def uploaded_file(file_collection):
    return UploadedFile.objects.create(
        file='test/test.txt',
        name='test.txt',
        file_type='text',
        collection=file_collection
    ) 
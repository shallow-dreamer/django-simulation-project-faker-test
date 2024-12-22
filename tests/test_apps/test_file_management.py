import pytest
from django.urls import reverse
from apps.file_management.models import FileCollection, UploadedFile
from apps.file_management.services import FileManagementService

pytestmark = pytest.mark.django_db

class TestFileManagementAPI:
    def test_create_collection(self, authenticated_client):
        url = reverse('filecollection-list')
        data = {
            'name': 'New Collection',
            'description': 'Test Description'
        }
        
        response = authenticated_client.post(url, data)
        assert response.status_code == 201
        assert response.data['name'] == 'New Collection'
    
    def test_add_file_to_collection(self, authenticated_client, file_collection):
        url = reverse('uploadedfile-add-to-collection', kwargs={'pk': 1})
        data = {'collection_id': file_collection.id}
        
        response = authenticated_client.post(url, data)
        assert response.status_code == 200

class TestFileManagementService:
    def test_handle_file_upload(self, tmp_path):
        # 创建测试文件
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        with open(test_file, 'rb') as f:
            result = FileManagementService.handle_file_upload(
                file=f,
                filename='test.txt',
                file_type='text'
            )
        
        assert isinstance(result, UploadedFile)
        assert result.name == 'test.txt' 
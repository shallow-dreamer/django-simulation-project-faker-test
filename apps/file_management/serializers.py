from rest_framework import serializers
from apps.file_management.models import FileCollection, UploadedFile
from apps.core.serializers import TimeStampedSerializer

class FileCollectionSerializer(TimeStampedSerializer):
    """
    文件收藏序列化器
    """
    class Meta:
        model = FileCollection
        fields = ['id', 'name', 'description', 'user', 'created_at', 'updated_at']
        read_only_fields = ['user']
        swagger_schema_fields = {
            "description": "文件收藏的序列化表示",
            "example": {
                "id": 1,
                "name": "示例收藏",
                "description": "这是一个示例收藏",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

class UploadedFileSerializer(TimeStampedSerializer):
    """
    上传文件序列化器
    """
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'name', 'file_type', 'collection', 
                 'created_at', 'updated_at']
        swagger_schema_fields = {
            "description": "上传文件的序列化表示",
            "example": {
                "id": 1,
                "file": "/media/uploads/example.txt",
                "name": "example.txt",
                "file_type": "text",
                "collection": 1,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        } 
from apps.core.views import BaseViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.file_management.models import FileCollection, UploadedFile
from apps.file_management.serializers import FileCollectionSerializer, UploadedFileSerializer

@extend_schema_view(
    list=extend_schema(
        summary="获取收藏列表",
        description="获取当前用户的所有文件收藏列表",
        tags=["file-management"]
    ),
    create=extend_schema(
        summary="创建新收藏",
        description="创建一个新的文件收藏",
        tags=["file-management"]
    )
)
class FileCollectionViewSet(BaseViewSet):
    """
    文件收藏管理视图集
    """
    queryset = FileCollection.objects.all()
    serializer_class = FileCollectionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

@extend_schema_view(
    list=extend_schema(
        summary="获取文件列表",
        description="获取所有上传的文件列表",
        tags=["file-management"]
    ),
    create=extend_schema(
        summary="上传新文件",
        description="上传一个新文件",
        tags=["file-management"]
    )
)
class UploadedFileViewSet(BaseViewSet):
    """
    文件上传管理视图集
    """
    queryset = UploadedFile.objects.all()
    serializer_class = UploadedFileSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="添加文件到收藏",
        description="将指定文件添加到指定的收藏中",
        tags=["file-management"]
    )
    @action(detail=True, methods=['post'])
    def add_to_collection(self, request, pk=None):
        file = self.get_object()
        collection_id = request.data.get('collection_id')
        
        try:
            collection = FileCollection.objects.get(
                id=collection_id, 
                user=request.user
            )
            file.collection = collection
            file.save()
            return Response({'status': 'file added to collection'})
        except FileCollection.DoesNotExist:
            return Response(
                {'error': 'Collection not found'}, 
                status=status.HTTP_404_NOT_FOUND
            ) 
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import ExternalFileReference
from .services import ExternalReferenceService
from .serializers import ExternalFileReferenceSerializer

class ExternalFileReferenceViewSet(viewsets.ModelViewSet):
    """
    外部文件引用视图集
    
    设计考虑：
    1. 提供外部文件引用的CRUD操作
    2. 支持文件引用的创建和管理
    3. 处理到外部平台的重定向
    4. 实现适当的错误处理和响应
    """
    queryset = ExternalFileReference.objects.all()
    serializer_class = ExternalFileReferenceSerializer

    def create(self, request):
        """
        创建外部文件引用
        
        功能：
        1. 验证请求数据
        2. 创建文件引用记录
        3. 可选地导入文件数据
        4. 返回创建结果
        """
        try:
            file_data = request.FILES.get('file')
            reference = ExternalReferenceService.create_reference(
                platform_name=request.data.get('platform_name'),
                external_url=request.data.get('external_url'),
                reference_id=request.data.get('reference_id'),
                file_name=request.data.get('file_name'),
                file_type=request.data.get('file_type'),
                user=request.user,
                file_data=file_data
            )
            return Response(
                self.serializer_class(reference).data,
                status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def view_source(self, request, pk=None):
        """
        重定向到源文件页面
        
        功能：
        1. 获取外部文件引用
        2. 重定向到原始平台
        3. 处理重定向异常
        """
        reference = self.get_object()
        return redirect(reference.external_url) 
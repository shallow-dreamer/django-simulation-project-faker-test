from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied

class SParameterFileViewSet(viewsets.ModelViewSet):
    # ... 其他代码 ...

    def download(self, request, pk=None):
        file_obj = self.get_object()
        if file_obj.source_type == 'EXTERNAL':
            raise PermissionDenied("External files must be downloaded from their original platform")
        # 处理本地文件下载... 
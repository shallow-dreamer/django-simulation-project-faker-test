from apps.core.views import BaseViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.parameter_processing.models import SParameter, ParameterHistory
from apps.parameter_processing.serializers import SParameterSerializer, ParameterHistorySerializer
from apps.parameter_processing.services import ParameterProcessingService
from apps.core.export_service import ExportService

@extend_schema_view(
    list=extend_schema(
        summary="获取S参数列表",
        description="获取所有S参数数据列表",
        tags=["parameter-processing"]
    ),
    create=extend_schema(
        summary="创建S参数",
        description="创建新的S参数数据",
        tags=["parameter-processing"]
    )
)
class SParameterViewSet(viewsets.ModelViewSet):
    """
    S参数管理视图集
    """
    queryset = SParameter.objects.all()
    serializer_class = SParameterSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="处理S参数",
        description="对指定的S参数进行处理",
        tags=["parameter-processing"],
        responses={200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "data": {"type": "object"}
            }
        }}
    )
    @action(detail=True, methods=['post'])
    def process_parameter(self, request, pk=None):
        parameter = self.get_object()
        service = ParameterProcessingService()
        result = service.process_parameter(parameter)
        return Response(result)

    @extend_schema(
        summary="删除S参数并记录历史",
        description="删除指定的S参数并记录删除历史",
        tags=["parameter-processing"]
    )
    @action(detail=True, methods=['post'])
    def delete_with_history(self, request, pk=None):
        parameter = self.get_object()
        ParameterHistory.objects.create(
            parameter=parameter,
            operation='delete',
            details=request.data.get('details', {})
        )
        parameter.delete()
        return Response({'status': 'parameter deleted'})

    @extend_schema(
        summary="导出参数数据",
        description="导出S参数数据为指定格式",
        parameters=[
            OpenApiParameter(
                name='format',
                type=str,
                location=OpenApiParameter.QUERY,
                description='导出格式 (csv/excel/touchstone)',
                required=True
            )
        ],
        tags=["parameter-processing"]
    )
    @action(detail=True, methods=['get'])
    def export(self, request, pk=None):
        parameter = self.get_object()
        export_format = request.query_params.get('format', 'csv')
        
        # 格式化数据
        data = ExportService.format_parameter_data(parameter.value)
        
        # 导出数据
        filename = f"parameter_{parameter.id}"
        return ExportService.export_data(data, export_format, filename) 
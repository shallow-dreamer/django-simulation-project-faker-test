from apps.core.views import BaseViewSet
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.com_simulation.models import ComSimulation, SimulationHistory
from apps.com_simulation.serializers import ComSimulationSerializer, SimulationHistorySerializer
from apps.com_simulation.services import SimulationService
from apps.core.export_service import ExportService
from rest_framework import status

@extend_schema_view(
    list=extend_schema(
        summary="获取仿真列表",
        description="获取所有仿真任务列表",
        tags=["simulation"]
    ),
    create=extend_schema(
        summary="创建仿真任务",
        description="创建新的仿真任务",
        tags=["simulation"]
    )
)
class ComSimulationViewSet(viewsets.ModelViewSet):
    """
    仿真管理视图集
    """
    queryset = ComSimulation.objects.all()
    serializer_class = ComSimulationSerializer
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        summary="运行仿真",
        description="启动指定的仿真任务",
        tags=["simulation"],
        responses={200: {
            "type": "object",
            "properties": {
                "status": {"type": "string"},
                "message": {"type": "string"}
            }
        }}
    )
    @action(detail=True, methods=['post'])
    def run_simulation(self, request, pk=None):
        simulation = self.get_object()
        service = SimulationService()
        
        try:
            result = service.run_simulation(simulation)
            return Response(result)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

    @extend_schema(
        summary="获取仿真状态",
        description="获取指定仿真任务的当前状态",
        tags=["simulation"]
    )
    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        simulation = self.get_object()
        service = SimulationService()
        status = service.get_simulation_status(simulation.id)
        return Response(status)

    @extend_schema(
        summary="导出仿真结果",
        description="导出仿真结果为指定格式",
        parameters=[
            OpenApiParameter(
                name='format',
                type=str,
                location=OpenApiParameter.QUERY,
                description='导出格式 (csv/excel)',
                required=True
            )
        ],
        tags=["simulation"]
    )
    @action(detail=True, methods=['get'])
    def export_results(self, request, pk=None):
        simulation = self.get_object()
        export_format = request.query_params.get('format', 'csv')
        
        if not simulation.result:
            return Response(
                {'error': 'No simulation results available'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # 格式化数据
        data = ExportService.format_simulation_data(simulation.result)
        
        # 导出数据
        filename = f"simulation_{simulation.id}"
        return ExportService.export_data(data, export_format, filename) 
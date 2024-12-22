from rest_framework import serializers
from .models import ComSimulation, SimulationHistory
from apps.core.serializers import TimeStampedSerializer

class ComSimulationSerializer(TimeStampedSerializer):
    """
    仿真序列化器
    """
    class Meta:
        model = ComSimulation
        fields = ['id', 'name', 'parameters', 'configuration', 'status', 
                 'result', 'created_at', 'updated_at']
        swagger_schema_fields = {
            "description": "仿真任务的序列化表示",
            "example": {
                "id": 1,
                "name": "示例仿真",
                "parameters": [1, 2],
                "configuration": {
                    "frequency_range": [0, 1000],
                    "step_size": 0.1
                },
                "status": "completed",
                "result": {"max_value": 0.5, "min_value": -0.5},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

class SimulationHistorySerializer(TimeStampedSerializer):
    """
    仿真历史记录序列化器
    """
    class Meta:
        model = SimulationHistory
        fields = ['id', 'simulation', 'execution_time', 'status', 
                 'error_message', 'created_at', 'updated_at']
        swagger_schema_fields = {
            "description": "仿真历史记录的序列化表示",
            "example": {
                "id": 1,
                "simulation": 1,
                "execution_time": 10.5,
                "status": "completed",
                "error_message": None,
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        } 
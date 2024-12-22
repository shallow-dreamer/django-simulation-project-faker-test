from rest_framework import serializers
from .models import SParameter, ParameterHistory
from apps.core.serializers import TimeStampedSerializer

class SParameterSerializer(TimeStampedSerializer):
    """
    S参数序列化器
    """
    class Meta:
        model = SParameter
        fields = ['id', 'file', 'frequency', 'value', 'created_at', 'updated_at']
        swagger_schema_fields = {
            "description": "S参数的序列化表示",
            "example": {
                "id": 1,
                "file": 1,
                "frequency": 1000.0,
                "value": {
                    "s11": {"real": 0.1, "imag": -0.2},
                    "s12": {"real": 0.3, "imag": -0.4}
                },
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        }

class ParameterHistorySerializer(TimeStampedSerializer):
    """
    参数历史记录序列化器
    """
    class Meta:
        model = ParameterHistory
        fields = ['id', 'parameter', 'operation', 'details', 'created_at', 'updated_at']
        swagger_schema_fields = {
            "description": "参数操作历史的序列化表示",
            "example": {
                "id": 1,
                "parameter": 1,
                "operation": "process",
                "details": {"action": "frequency_filter", "threshold": 1000},
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z"
            }
        } 
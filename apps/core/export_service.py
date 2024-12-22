from typing import Any, Dict, List, Optional
from django.http import HttpResponse
from .exporters import CSVExporter, ExcelExporter, TouchstoneExporter

class ExportService:
    """
    导出服务
    """
    EXPORTERS = {
        'csv': CSVExporter,
        'excel': ExcelExporter,
        'touchstone': TouchstoneExporter
    }
    
    @classmethod
    def export_data(cls, data: Any, format: str, filename: str) -> HttpResponse:
        """
        导出数据
        """
        exporter_class = cls.EXPORTERS.get(format.lower())
        if not exporter_class:
            raise ValueError(f"Unsupported export format: {format}")
        
        exporter = exporter_class(data, filename)
        return exporter.export()
    
    @staticmethod
    def format_parameter_data(parameter: Dict) -> Dict:
        """
        格式化参数数据用于导出
        """
        return {
            'frequency': parameter['frequency'],
            's_parameters': [
                [parameter['value'][f's{i}{j}'] for j in range(1, 3)]
                for i in range(1, 3)
            ]
        }
    
    @staticmethod
    def format_simulation_data(simulation: Dict) -> List[Dict]:
        """
        格式化仿真数据用于导出
        """
        formatted_data = []
        for freq, result in zip(simulation['frequency'], simulation['results']):
            row = {
                'Frequency': freq,
                'Insertion_Loss': result.get('insertion_loss', 0),
                'Return_Loss': result.get('return_loss', 0),
                'Phase': result.get('phase', 0)
            }
            formatted_data.append(row)
        return formatted_data 
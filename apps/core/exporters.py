from typing import Any, Dict, List, Optional
import csv
import json
import xlsxwriter
from io import BytesIO
from abc import ABC, abstractmethod
from django.http import HttpResponse

class BaseExporter(ABC):
    """
    导出器基类
    """
    def __init__(self, data: Any, filename: str):
        self.data = data
        self.filename = filename
    
    @abstractmethod
    def export(self) -> HttpResponse:
        """导出数据"""
        pass

class CSVExporter(BaseExporter):
    """
    CSV导出器
    """
    def export(self) -> HttpResponse:
        output = BytesIO()
        writer = csv.writer(output)
        
        # 写入表头
        if isinstance(self.data, list) and self.data:
            headers = self.data[0].keys()
            writer.writerow(headers)
            
            # 写入数据
            for row in self.data:
                writer.writerow(row.values())
        
        response = HttpResponse(output.getvalue(), content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}.csv"'
        return response

class ExcelExporter(BaseExporter):
    """
    Excel导出器
    """
    def export(self) -> HttpResponse:
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # 写入表头
        if isinstance(self.data, list) and self.data:
            headers = list(self.data[0].keys())
            for col, header in enumerate(headers):
                worksheet.write(0, col, header)
            
            # 写入数据
            for row, data in enumerate(self.data, start=1):
                for col, value in enumerate(data.values()):
                    worksheet.write(row, col, value)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{self.filename}.xlsx"'
        return response

class TouchstoneExporter(BaseExporter):
    """
    Touchstone格式导出器
    """
    def export(self) -> HttpResponse:
        output = []
        
        # 添加文件头
        output.append("! Touchstone file")
        output.append("# Hz S RI R 50")
        
        # 写入数据
        for freq, s_params in zip(self.data['frequency'], self.data['s_parameters']):
            row = [f"{freq:.6e}"]
            for s in s_params:
                row.extend([f"{s.real:.6e}", f"{s.imag:.6e}"])
            output.append(" ".join(row))
        
        content = "\n".join(output)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{self.filename}.s2p"'
        return response 
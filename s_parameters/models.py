from django.db import models
from files.models import BaseFile

class SParameterFile(BaseFile):
    """
    S参数文件模型
    
    设计考虑：
    1. 继承BaseFile获取基础文件功能
    2. 添加S参数特有的属性
    3. 支持文件来源的追踪
    4. 便于与其他模型（如Com仿真）关联
    """
    frequency_range = models.CharField(max_length=100)  # 频率范围
    port_number = models.IntegerField()  # 端口数量
    format_type = models.CharField(max_length=50)  # 文件格式类型
    
    class Meta:
        db_table = 's_parameter_files'

class SParameterHistory(models.Model):
    """
    S参数处理历史记录
    
    设计考虑：
    1. 记录S参数文件的处理历史
    2. 保存处理操作和结果
    3. 支持历史追踪和回溯
    4. 便于问题排查和数据分析
    """
    s_parameter_file = models.ForeignKey(SParameterFile, on_delete=models.CASCADE)
    operation = models.CharField(max_length=50)  # 操作类型
    parameters = models.JSONField()  # 操作参数
    result = models.TextField()  # 操作结果
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 's_parameter_history' 
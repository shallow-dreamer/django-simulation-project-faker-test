from django.db import models
from files.models import BaseFile
from s_parameters.models import SParameterFile

class ComFile(BaseFile):
    """
    Com仿真文件模型
    
    设计考虑：
    1. 继承BaseFile，获取基础文件功能
    2. 关联S参数文件，支持仿真依赖
    3. 使用JSONField存储仿真参数，提供灵活性
    4. 记录仿真状态和结果
    """
    s_parameter_file = models.ForeignKey(SParameterFile, on_delete=models.SET_NULL, null=True)
    simulation_type = models.CharField(max_length=50)
    parameters = models.JSONField()  # 仿真参数配置

    class Meta:
        db_table = 'com_files'

class ComSimulationResult(models.Model):
    """
    Com仿真结果模型
    
    设计考虑：
    1. 记录仿真结果和状态
    2. 使用JSONField存储复杂的结果数据
    3. 关联到对应的Com文件
    4. 支持结果的时间追踪
    """
    com_file = models.ForeignKey(ComFile, on_delete=models.CASCADE)
    result_data = models.JSONField()  # 仿真结果数据
    status = models.CharField(max_length=20)  # 仿真状态
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'com_simulation_results' 
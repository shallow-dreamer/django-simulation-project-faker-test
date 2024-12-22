from django.db import models
from files.models import BaseFile
from com_simulation.models import ComFile

class SerderFile(BaseFile):
    """
    Serder仿真文件模型
    
    设计考虑：
    1. 继承BaseFile获取基础文件功能
    2. 关联Com仿真文件，建立依赖关系
    3. 使用JSONField存储复杂的仿真参数
    4. 支持仿真状态跟踪
    """
    com_file = models.ForeignKey(ComFile, on_delete=models.SET_NULL, null=True)  # 关联的Com文件
    simulation_parameters = models.JSONField()  # 仿真参数配置
    status = models.CharField(max_length=20)  # 仿真状态

    class Meta:
        db_table = 'serder_files'

class SerderSimulationResult(models.Model):
    """
    Serder仿真结果模型
    
    设计考虑：
    1. 存储仿真结果数据
    2. 关联对应的Serder文件
    3. 记录仿真时间信息
    4. 支持结果状态追踪
    """
    serder_file = models.ForeignKey(SerderFile, on_delete=models.CASCADE)
    result_data = models.JSONField()  # 仿真结果数据
    status = models.CharField(max_length=20)  # 结果状态
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True)  # 完成时间

    class Meta:
        db_table = 'serder_simulation_results' 
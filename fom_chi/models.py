from django.db import models
from files.models import BaseFile
from com_simulation.models import ComFile

class FomChiFile(BaseFile):
    """
    Fom_chi计算文件模型
    
    设计考虑：
    1. 继承BaseFile获取基础文件功能
    2. 关联Com仿真文件，支持数据依赖
    3. 存储计算参数和配置
    4. 跟踪计算状态
    """
    com_file = models.ForeignKey(ComFile, on_delete=models.SET_NULL, null=True)  # 关联的Com文件
    calculation_parameters = models.JSONField()  # 计算参数
    status = models.CharField(max_length=20)  # 计算状态

    class Meta:
        db_table = 'fom_chi_files'

class FomChiResult(models.Model):
    """
    Fom_chi计算结果模型
    
    设计考虑：
    1. 存储计算结果数据
    2. 关联对应的Fom_chi文件
    3. 记录计算时间信息
    4. 支持结果验证和分析
    """
    fom_chi_file = models.ForeignKey(FomChiFile, on_delete=models.CASCADE)
    result_data = models.JSONField()  # 计算结果数据
    status = models.CharField(max_length=20)  # 结果状态
    created_at = models.DateTimeField(auto_now_add=True)
    validation_status = models.CharField(max_length=20, null=True)  # 结果验证状态

    class Meta:
        db_table = 'fom_chi_results' 
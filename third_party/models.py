from django.db import models
from users.models import User

class ExternalPlatform(models.Model):
    """
    外部平台配置模型
    
    设计考虑：
    1. 支持多个外部平台的配置管理
    2. 可以随时启用/禁用特定平台
    3. 记录平台的基本信息和访问URL
    """
    name = models.CharField(max_length=100, unique=True)
    base_url = models.URLField()  # 平台的基础URL
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)  # 控制平台是否可用

    class Meta:
        db_table = 'external_platforms'

class ExternalFileReference(models.Model):
    """
    外部文件引用模型
    
    设计考虑：
    1. 记录外部文件的元数据和引用信息
    2. 不直接存储文件内容，而是保存引用关系
    3. 支持文件类型的区分，便于分类管理
    4. 记录创建者信息，便于追踪
    """
    platform = models.ForeignKey(ExternalPlatform, on_delete=models.CASCADE)
    external_url = models.URLField()  # 文件在外部平台的URL
    reference_id = models.CharField(max_length=255)  # 外部平台的文件标识符
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)  # 文件类型(s_parameter, com等)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'external_file_references'
        unique_together = ('platform', 'reference_id')  # 确保同一平台的文件引用唯一
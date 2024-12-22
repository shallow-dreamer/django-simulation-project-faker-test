from django.db import models
from users.models import User

class BaseFile(models.Model):
    """
    文件基类，作为所有文件类型的抽象基类
    
    设计考虑：
    1. 使用抽象基类减少代码重复，所有文件类型都继承这个基类
    2. 添加source_type区分文件来源，支持本地上传和外部平台导入
    3. 对于外部平台的文件，保存原始URL和引用ID以保持可追溯性
    4. 文件所有权关联到用户，便于权限控制
    """
    FILE_SOURCE_CHOICES = (
        ('LOCAL', '本地上传'),    # 本地上传的文件
        ('EXTERNAL', '外部平台'),  # 从外部平台导入的文件
    )

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')  # 实际存储的文件
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 文件所有者
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField(blank=True)
    
    # 文件来源相关字段
    source_type = models.CharField(max_length=20, choices=FILE_SOURCE_CHOICES)
    source_url = models.URLField(null=True, blank=True)  # 外部文件的原始URL
    source_reference = models.CharField(max_length=255, null=True, blank=True)  # 外部平台的文件标识

    class Meta:
        abstract = True  # 设置为抽象基类，不会创建实际的数据表

class FileVersion(models.Model):
    """
    文件版本控制模型
    
    设计考虑：
    1. 支持文件的版本管理
    2. 记录版本变更说明
    3. 保存各个版本的实际文件内容
    """
    file = models.ForeignKey('File', on_delete=models.CASCADE)
    version = models.CharField(max_length=50)
    content = models.FileField(upload_to='versions/')
    created_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)
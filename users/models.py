from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    用户模型
    
    设计考虑：
    1. 继承Django的AbstractUser，保留基础用户功能
    2. 扩展用户属性，添加组织和角色信息
    3. 记录用户创建时间，便于用户管理
    4. 支持基本的用户角色区分
    """
    organization = models.CharField(max_length=100)  # 用户所属组织
    role = models.CharField(max_length=20, choices=[
        ('admin', '管理员'),
        ('user', '普通用户'),
    ])  # 用户角色
    created_at = models.DateTimeField(auto_now_add=True)  # 用户创建时间 
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from users.models import User

class Collection(models.Model):
    """
    收藏模型
    
    设计考虑：
    1. 使用ContentType实现通用的收藏功能
    2. 支持收藏任意类型的文件
    3. 记录收藏创建时间，便于管理
    4. 确保用户对同一对象只能收藏一次
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 收藏的用户
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # 收藏对象的类型
    object_id = models.PositiveIntegerField()  # 收藏对象的ID
    content_object = GenericForeignKey('content_type', 'object_id')  # 收藏的具体对象
    created_at = models.DateTimeField(auto_now_add=True)  # 收藏时间
    
    class Meta:
        db_table = 'collections'
        unique_together = ('user', 'content_type', 'object_id')  # 确保不重复收藏

class CollectionFolder(models.Model):
    """
    收藏文件夹模型
    
    设计考虑：
    1. 支持收藏的层级组织
    2. 允许用户创建个性化的收藏分类
    3. 通过parent字段实现文件夹嵌套
    4. 记录创建时间，便于管理
    """
    name = models.CharField(max_length=255)  # 文件夹名称
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 所属用户
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)  # 父文件夹
    created_at = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'collection_folders'
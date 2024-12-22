from rest_framework import permissions

class IsFileOwner(permissions.BasePermission):
    """
    文件所有者权限检查
    
    设计考虑：
    1. 确保只有文件所有者才能访问或修改文件
    2. 继承DRF的BasePermission，便于权限系统集成
    3. 支持对象级别的权限控制
    """
    def has_object_permission(self, request, view, obj):
        # 检查请求用户是否为文件所有者
        return obj.user == request.user 
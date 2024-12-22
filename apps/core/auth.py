from rest_framework import authentication, exceptions
from rest_framework.permissions import BasePermission
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

class TokenAuthentication(authentication.TokenAuthentication):
    """
    自定义Token认证
    """
    keyword = 'Bearer'

class IsOwner(BasePermission):
    """
    对象所有者权限
    """
    def has_object_permission(self, request, view, obj):
        return hasattr(obj, 'user') and obj.user == request.user 

class DocumentationAuthentication(authentication.BaseAuthentication):
    """
    允许文档页面的认证类
    """
    def authenticate(self, request):
        # 检查是否是文档相关的路径
        if request.path.startswith('/api/docs/') or \
           request.path.startswith('/api/redoc/') or \
           request.path.startswith('/api/schema/'):
            return (AnonymousUser(), None)
        return None
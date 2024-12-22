from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .auth import DocumentationAuthentication
from django.views.generic import RedirectView
from django.urls import reverse

class BaseViewSet(viewsets.ModelViewSet):
    """
    基础视图集
    """
    authentication_classes = [DocumentationAuthentication]
    permission_classes = [IsAuthenticated] 

class APIRootView(RedirectView):
    """
    API根路径视图
    """
    def get_redirect_url(self, *args, **kwargs):
        return reverse('api:swagger-ui')
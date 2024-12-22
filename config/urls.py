from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from apps.file_management.views import FileCollectionViewSet, UploadedFileViewSet
from apps.parameter_processing.views import SParameterViewSet
from apps.com_simulation.views import ComSimulationViewSet
from apps.core.views import APIRootView

router = DefaultRouter()
router.register(r'collections', FileCollectionViewSet)
router.register(r'files', UploadedFileViewSet)
router.register(r'parameters', SParameterViewSet)
router.register(r'simulations', ComSimulationViewSet)

api_urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [
    path('api/', include((api_urlpatterns, 'api'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', APIRootView.as_view(), name='api-root'),
]
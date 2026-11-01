# apps/systems/integrations/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.integration_views import IntegrationProfileViewSet

router = DefaultRouter()
router.register(r'configs', IntegrationProfileViewSet, basename='integrations-config')

urlpatterns = [
    path('', include(router.urls)),
]
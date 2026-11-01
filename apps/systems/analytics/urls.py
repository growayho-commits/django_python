# apps/systems/analytics/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.analytics_views import AnalyticsProfileViewSet

router = DefaultRouter()
router.register(r'metrics', AnalyticsProfileViewSet, basename='analytics-metrics')

urlpatterns = [
    path('', include(router.urls)),
]
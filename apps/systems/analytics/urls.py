from django.urls import path
from .views.analytics_views import AnalyticsProfileViewSet

app_name = 'analytics'

urlpatterns = [
    path('profile/', AnalyticsProfileViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='profile'),
]

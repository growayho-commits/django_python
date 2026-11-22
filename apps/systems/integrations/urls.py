from django.urls import path
from .views.integration_views import IntegrationProfileViewSet

app_name = 'integrations'

urlpatterns = [
    path('integration-profile/', IntegrationProfileViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='integration_profile'),
]

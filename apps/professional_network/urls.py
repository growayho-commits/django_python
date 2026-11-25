from django.urls import include, path

from .views.professional_views import ProfessionalProfileViewSet, ServiceRequestViewSet
from .views.service_portal_views import (
    service_directory_view,
    service_provider_detail_view,
    service_workspace_view,
)

app_name = 'professional_network'

urlpatterns = [
    path('enquiries/', include('apps.professional_network.enquiries.urls')),
    path('profiles/', include('apps.professional_network.profiles.urls')),
    path('ratings/', include('apps.professional_network.ratings.urls')),
    path('search_engine/', include('apps.professional_network.search_engine.urls')),
    path('service_categries/', include('apps.professional_network.service_categries.urls')),
    path('portal/', service_directory_view, name='service_directory'),
    path('portal/provider/<int:pk>/', service_provider_detail_view, name='service_provider_detail'),
    path('portal/workspace/', service_workspace_view, name='service_workspace'),
    path('professional-profile/', ProfessionalProfileViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='professional_profile'),
    path('service-request/', ServiceRequestViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_request'),
]
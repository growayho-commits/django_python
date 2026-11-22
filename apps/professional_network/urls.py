from django.urls import path, include
from .views.professional_views import ProfessionalProfileViewSet, ServiceRequestViewSet

app_name = 'professional_network'

urlpatterns = [
    path('enquiries/', include('apps.professional_network.enquiries.urls')),
    path('profiles/', include('apps.professional_network.profiles.urls')),
    path('ratings/', include('apps.professional_network.ratings.urls')),
    path('search_engine/', include('apps.professional_network.search_engine.urls')),
    path('service_categries/', include('apps.professional_network.service_categries.urls')),
    path('professional-profile/', ProfessionalProfileViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='professional_profile'),
    path('service-request/', ServiceRequestViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_request'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.professional_network.views import ProfessionalProfileViewSet, ServiceRequestViewSet

router = DefaultRouter()
router.register(r'profiles', ProfessionalProfileViewSet, basename='professional-profile')
router.register(r'service-requests', ServiceRequestViewSet, basename='service-request')

urlpatterns = [
    path('', include(router.urls)),
]
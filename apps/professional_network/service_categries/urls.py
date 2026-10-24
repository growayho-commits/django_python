from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.professional_network.service_categries.views.service_categries_views import (
    ServiceCategoryViewSet,
    ServiceAttributeViewSet,
    ServiceListingViewSet,
    ServiceVariationPlanViewSet,
)

router = DefaultRouter()
router.register(r'categories', ServiceCategoryViewSet)
router.register(r'attributes', ServiceAttributeViewSet)
router.register(r'listings', ServiceListingViewSet)
router.register(r'plans', ServiceVariationPlanViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
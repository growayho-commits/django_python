from django.urls import path
from .views.service_categries_views import ServiceCategoryViewSet, ServiceAttributeViewSet, ServiceListingViewSet, ServiceVariationPlanViewSet

app_name = 'service_categries'

urlpatterns = [
    path('service-category/', ServiceCategoryViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_category'),
    path('service-attribute/', ServiceAttributeViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_attribute'),
    path('service-listing/', ServiceListingViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_listing'),
    path('service-variation-plan/', ServiceVariationPlanViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='service_variation_plan'),
]

from rest_framework import viewsets, filters
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from apps.professional_network.service_categries.models import (
    ServiceCategory,
    ServiceAttribute,
    ServiceListing,
    ServiceVariationPlan,
)
from apps.professional_network.service_categries.serializers import (
    ServiceCategorySerializer,
    ServiceAttributeSerializer,
    ServiceListingSerializer,
    ServiceVariationPlanSerializer,
)


class ServiceCategoryViewSet(viewsets.ModelViewSet):
    queryset = ServiceCategory.objects.all()
    serializer_class = ServiceCategorySerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['parent', 'is_active', 'sac_code']
    search_fields = ['name', 'google_business_category', 'sac_code']


class ServiceAttributeViewSet(viewsets.ModelViewSet):
    queryset = ServiceAttribute.objects.all()
    serializer_class = ServiceAttributeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title']


class ServiceListingViewSet(viewsets.ModelViewSet):
    queryset = ServiceListing.objects.all()
    serializer_class = ServiceListingSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category']
    search_fields = ['title', 'description']


class ServiceVariationPlanViewSet(viewsets.ModelViewSet):
    queryset = ServiceVariationPlan.objects.all()
    serializer_class = ServiceVariationPlanSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['service', 'price']
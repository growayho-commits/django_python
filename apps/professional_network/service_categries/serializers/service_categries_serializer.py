from rest_framework import serializers
from apps.professional_network.service_categries.models import (
    ServiceCategory,
    ServiceAttribute,
    ServiceListing,
    ServiceVariationPlan,
)


class ServiceAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAttribute
        fields = ['id', 'category', 'title']


class ServiceVariationPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceVariationPlan
        fields = ['id', 'service', 'plan_name', 'description', 'price', 'estimated_duration']


class ServiceListingSerializer(serializers.ModelSerializer):
    plans = ServiceVariationPlanSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceListing
        fields = ['id', 'title', 'category', 'description', 'created_at', 'plans']


class ServiceCategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    service_attributes = ServiceAttributeSerializer(many=True, read_only=True)
    services = ServiceListingSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceCategory
        fields = [
            'id', 'name', 'parent', 'google_business_category', 
            'sac_code', 'is_active', 'subcategories', 'service_attributes', 'services'
        ]
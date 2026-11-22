from rest_framework import serializers
from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile

class PricingExtraSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingExtraProfile
        fields = ['id', 'extra_name', 'extra_code', 'additional_fee', 'is_mandatory', 'created_at', 'updated_at']
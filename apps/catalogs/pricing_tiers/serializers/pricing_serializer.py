# apps/catalogs/pricing_tiers/serializers/pricing_serializer.py

from rest_framework import serializers
from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingProfile
        fields = ['id', 'catalog', 'tier_name', 'base_price', 'bulk_min_qty', 'discount_percentage', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
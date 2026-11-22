from rest_framework import serializers
from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile

class PricingTierSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingTierProfile
        fields = ['id', 'tier_name', 'min_quantity', 'max_quantity', 'discount_percentage', 'is_active', 'created_at', 'updated_at']
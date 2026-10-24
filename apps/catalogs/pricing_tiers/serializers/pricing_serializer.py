from rest_framework import serializers
from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PricingProfile
        fields = '__all__'

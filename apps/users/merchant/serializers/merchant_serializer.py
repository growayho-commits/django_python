from rest_framework import serializers
from apps.users.merchant.models import MerchantProfile

class MerchantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantProfile
        fields = ['id', 'user', 'business_name', 'merchant_type', 'gstin', 'is_verified', 'created_at', 'updated_at']
        read_only_fields = ['id', 'is_verified', 'created_at', 'updated_at']
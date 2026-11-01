from rest_framework import serializers
from ..models.gateway_profile import PaymentGatewayConfig

class PaymentGatewayConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGatewayConfig
        fields = ['id', 'gateway_name', 'is_active', 'api_key', 'api_secret', 'created_at', 'updated_at']
        extra_kwargs = {'api_secret': {'write_only': True}}
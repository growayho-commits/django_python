# apps/marketing_leads/checkout_flows/serializers/checkout_serializer.py

from rest_framework import serializers
from ..models.checkout_profile import CheckoutProfile

class CheckoutProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckoutProfile
        fields = ['id', 'user', 'cart_id', 'status', 'shipping_address', 'payment_method', 'total_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
# apps/marketing_leads/orders/serializers/order_serializer.py

from rest_framework import serializers
from ..models.order_profile import OrderProfile, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'product_id', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id']

class OrderProfileSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = OrderProfile
        fields = ['id', 'user', 'order_number', 'status', 'total_amount', 'shipping_address', 'billing_address', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'order_number', 'created_at', 'updated_at']
from rest_framework import serializers
from apps.marketing_leads.orders.models import OrderProfile, OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class OrderProfileSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True, source='orderitem_set')

    class Meta:
        model = OrderProfile
        fields = [
            'id', 'user', 'status', 'total_amount', 'shipping_address', 
            'billing_address', 'items', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']
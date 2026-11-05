from rest_framework import serializers
from apps.marketing_leads.carts.models import CartProfile, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'quantity', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CartProfileSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True, source='cartitem_set')

    class Meta:
        model = CartProfile
        fields = ['id', 'user', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
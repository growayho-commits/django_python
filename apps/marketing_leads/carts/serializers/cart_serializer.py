# apps/marketing_leads/carts/serializers/cart_serializer.py

from rest_framework import serializers
from ..models.cart_profile import CartProfile, CartItem

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product_id', 'quantity', 'unit_price', 'created_at']
        read_only_fields = ['id', 'created_at']

class CartProfileSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = CartProfile
        fields = ['id', 'user', 'session_id', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
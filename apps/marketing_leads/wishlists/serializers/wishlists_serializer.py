# apps/marketing_leads/wishlists/serializers/wishlists_serializer.py

from rest_framework import serializers
from ..models.wishlists_profile import WishlistProfile

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProfile
        fields = ['id', 'user', 'product_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
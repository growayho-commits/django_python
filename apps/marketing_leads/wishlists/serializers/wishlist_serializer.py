from rest_framework import serializers
from apps.marketing_leads.wishlists.models import Wishlist

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'product_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
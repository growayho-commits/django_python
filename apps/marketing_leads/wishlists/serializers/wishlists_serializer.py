from rest_framework import serializers
from apps.catalogs.wishlists.models.wishlists_profile import WishlistProfile

class WishlistProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistProfile
        fields = '__all__'

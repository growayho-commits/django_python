from rest_framework import serializers
from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile

class CatalogWishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogWishlistProfile
        fields = ['id', 'user_identifier', 'product_sku', 'notes', 'created_at', 'updated_at']
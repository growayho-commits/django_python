from rest_framework import serializers
from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogVariantProfile
        fields = ['id', 'product_name', 'variant_sku', 'color', 'size', 'price_override', 'is_active', 'created_at', 'updated_at']
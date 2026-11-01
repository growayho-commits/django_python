# apps/catalogs/variants/serializers/variant_serializer.py

from rest_framework import serializers
from apps.catalogs.variants.models.variant_profile import CatalogVariantProfile

class CatalogVariantProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogVariantProfile
        fields = ['id', 'catalog', 'variant_name', 'sku', 'price_override', 'stock_quantity', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
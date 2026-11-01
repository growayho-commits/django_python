# apps/catalogs/core_catalogs/serializers/core_catalog_serializer.py

from rest_framework import serializers
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CoreCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreCatalog
        fields = ['id', 'name', 'sku', 'brand', 'description', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
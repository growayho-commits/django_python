# apps/catalogs/catalog_statuses/serializers/status_serializer.py

from rest_framework import serializers
from apps.catalogs.catalog_statuses.models.status_profile import CatalogStatusProfile

class CatalogStatusProfileSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = CatalogStatusProfile
        fields = ['id', 'catalog', 'status', 'status_display', 'remarks', 'updated_at']
        read_only_fields = ['id', 'updated_at']
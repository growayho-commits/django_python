from rest_framework import serializers
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogStatusProfile
        fields = ['id', 'status_name', 'status_code', 'description', 'is_default', 'created_at', 'updated_at']
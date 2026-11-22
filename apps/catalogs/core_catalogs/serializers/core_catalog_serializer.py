from rest_framework import serializers
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile

class CoreCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreCatalogProfile
        fields = [
            'id', 
            'name', 
            'description', 
            'unit', 
            'is_active', 
            'created_at', 
            'updated_at'
        ]
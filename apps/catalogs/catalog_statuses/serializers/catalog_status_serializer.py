from rest_framework import serializers
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogStatusProfile
        fields = '__all__'

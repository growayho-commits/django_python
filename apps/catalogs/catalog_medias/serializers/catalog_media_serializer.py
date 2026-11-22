from rest_framework import serializers
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMediaProfile
        fields = ['id', 'title', 'media_url', 'media_type', 'is_primary', 'created_at', 'updated_at']
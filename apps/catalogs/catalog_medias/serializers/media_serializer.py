# apps/catalogs/catalog_medias/serializers/media_serializer.py

from rest_framework import serializers
from apps.catalogs.catalog_medias.models.media_profile import CatalogMediaProfile

class CatalogMediaProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMediaProfile
        fields = ['id', 'catalog', 'image', 'alt_text', 'is_primary', 'created_at']
        read_only_fields = ['id', 'created_at']
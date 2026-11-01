from rest_framework import serializers
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogMediaProfile
        fields = '__all__'

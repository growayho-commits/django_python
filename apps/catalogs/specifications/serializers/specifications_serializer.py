# apps/catalogs/specifications/serializers/specifications_serializer.py

from rest_framework import serializers
from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile

class SpecificationsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationsProfile
        fields = ['id', 'catalog', 'spec_key', 'spec_value', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
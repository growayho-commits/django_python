# apps/catalogs/attributes/serializers/attribute_serializer.py

from rest_framework import serializers
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeProfile
        fields = ['id', 'catalog', 'attribute_name', 'attribute_value', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
from rest_framework import serializers
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeProfile
        fields = ['id', 'name', 'code', 'data_type', 'is_required', 'created_at', 'updated_at']
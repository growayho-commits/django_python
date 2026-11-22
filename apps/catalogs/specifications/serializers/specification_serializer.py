from rest_framework import serializers
from apps.catalogs.specifications.models.specification_profile import SpecificationProfile

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationProfile
        fields = ['id', 'title', 'value', 'unit', 'created_at', 'updated_at']
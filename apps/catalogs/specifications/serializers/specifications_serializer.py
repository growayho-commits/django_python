from rest_framework import serializers
from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile

class SpecificationsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecificationsProfile
        fields = '__all__'

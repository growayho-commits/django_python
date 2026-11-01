# apps/catalogs/bundles_kits/serializers/bundle_serializer.py

from rest_framework import serializers
from apps.catalogs.bundles_kits.models.bundle_profile import BundleProfile

class BundleProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleProfile
        fields = ['id', 'bundle_name', 'description', 'items', 'bundle_price', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
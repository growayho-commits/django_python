from rest_framework import serializers
from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile

class BundleKitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundleKitProfile
        fields = ['id', 'bundle_name', 'bundle_sku', 'bundle_price', 'is_active', 'created_at', 'updated_at']

from rest_framework import serializers
from apps.catalogs.bundles_kits.models.bundles_kits_profile import BundlesKitsProfile

class BundlesKitsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BundlesKitsProfile
        fields = '__all__'

from rest_framework import serializers
from apps.catalogs.core_catalogs.models import CoreCatalog

class CoreCatalogSerializer(serializers.ModelSerializer):
    vendor_email = serializers.ReadOnlyField(source='vendor.email')

    class Meta:
        model = CoreCatalog
        fields = [
            'id', 'vendor', 'vendor_email', 'title', 'description', 
            'sku', 'price', 'stock', 'visibility', 'is_active', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'vendor', 'created_at', 'updated_at']

    def create(self, validated_data):
        # தற்போதைய லாகின் செய்த பயனரை (Merchant அல்லது Seller) வெண்டராகப் பதிவு செய்தல்
        validated_data['vendor'] = self.context['request'].user
        return super().create(validated_data)
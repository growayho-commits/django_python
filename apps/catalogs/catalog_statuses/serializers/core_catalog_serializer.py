from rest_framework import serializers
from apps.catalog.core_catalog.models.core_catalog_profile import CoreCatalog

class CoreCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoreCatalog
        fields = [
            'id', 'catalog_code', 'title', 'slug', 'catalog_type',
            'brand_name', 'brand_logo_url', 'root_category', 'sub_category',
            'leaf_category', 'short_description', 'long_description',
            'hsn_or_sac_code', 'gst_percentage', 'country_of_origin',
            'is_active', 'is_featured', 'is_draft', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
[cite: 1]
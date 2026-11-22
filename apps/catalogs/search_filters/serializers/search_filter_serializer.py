from rest_framework import serializers
from apps.catalogs.search_filters.models.search_filter_profile import SearchFilterProfile

class SearchFilterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFilterProfile
        fields = ['id', 'filter_name', 'filter_key', 'filter_type', 'is_active', 'created_at', 'updated_at']
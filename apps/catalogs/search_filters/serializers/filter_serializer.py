# apps/catalogs/search_filters/serializers/filter_serializer.py

from rest_framework import serializers
from apps.catalogs.search_filters.models.filter_profile import SearchFilterProfile

class SearchFilterProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFilterProfile
        fields = ['id', 'category', 'filter_name', 'filter_key', 'filter_options', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
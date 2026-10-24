from rest_framework import serializers
from apps.catalogs.search_filters.models.search_filters_profile import SearchFiltersProfile

class SearchFiltersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchFiltersProfile
        fields = '__all__'

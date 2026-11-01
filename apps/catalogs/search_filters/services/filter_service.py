# apps/catalogs/search_filters/services/filter_service.py

from apps.catalogs.search_filters.models.filter_profile import SearchFilterProfile

class SearchFilterService:
    @staticmethod
    def create_filter(validated_data):
        """புதிய தேடல் வடிப்பானைச் சேர்க்க (Add Search Filter)"""
        return SearchFilterProfile.objects.create(**validated_data)

    @staticmethod
    def update_filter(filter_id, validated_data):
        """தேடல் வடிப்பானைப் புதுப்பிக்க (Edit / Update)"""
        try:
            filter_obj = SearchFilterProfile.objects.get(id=filter_id)
            for key, value in validated_data.items():
                setattr(filter_obj, key, value)
            filter_obj.save()
            return filter_obj
        except SearchFilterProfile.DoesNotExist:
            raise ValueError("Search filter profile does not exist.")
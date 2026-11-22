from apps.catalogs.search_filters.models.search_filter_profile import SearchFilterProfile

class SearchFilterApplicationService:
    @staticmethod
    def get_all_filters():
        return SearchFilterProfile.objects.all()

    @staticmethod
    def create_filter(validated_data):
        return SearchFilterProfile.objects.create(**validated_data)
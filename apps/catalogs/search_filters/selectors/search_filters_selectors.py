from apps.catalogs.search_filters.models.search_filters_profile import SearchFiltersProfile

class SearchFiltersSelector:
    @staticmethod
    def get_filters_by_catalog(catalog_id: str) -> SearchFiltersProfile | None:
        return SearchFiltersProfile.objects.filter(catalog_id=catalog_id).first()

from apps.catalogs.search_filters.models.search_filter_profile import SearchFilterProfile

def get_active_search_filters():
    return SearchFilterProfile.objects.filter(is_active=True)
from django.db import transaction
from apps.catalogs.search_filters.dtos.search_filters_dtos import SearchFiltersCreateDTO
from apps.catalogs.search_filters.models.search_filters_profile import SearchFiltersProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class SearchFiltersApplicationService:
    @staticmethod
    @transaction.atomic
    def save_search_filters(dto: SearchFiltersCreateDTO) -> SearchFiltersProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        return SearchFiltersProfile.save_filters(catalog_obj=catalog, dto=dto)

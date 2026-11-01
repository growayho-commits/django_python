from django.shortcuts import get_object_or_404
from apps.catalog.core_catalog.models.core_catalog_profile import CoreCatalog

class CoreCatalogSelector:
    """
    Read-only operations for Core Catalog adhering to CQRS principles[cite: 1].
    """
    @staticmethod
    def get_catalog_by_id(catalog_id: str) -> CoreCatalog:
        return get_object_or_404(CoreCatalog, id=catalog_id, is_active=True)

    @staticmethod
    def get_active_catalogs_by_category(root_category: str):
        return CoreCatalog.objects.filter(root_category=root_category, is_active=True, is_draft=False)

    @staticmethod
    def filter_catalogs_by_search_query(query: str):
        return CoreCatalog.objects.filter(
            models.Q(title__icontains=query) | 
            models.Q(catalog_code__icontains=query) |
            models.Q(short_description__icontains=query),
            is_active=True
        )
[cite: 1]
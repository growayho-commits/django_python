from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusSelector:
    @staticmethod
    def get_status_by_catalog(catalog_id: str) -> CatalogStatusProfile | None:
        return CatalogStatusProfile.objects.filter(catalog_id=catalog_id).first()

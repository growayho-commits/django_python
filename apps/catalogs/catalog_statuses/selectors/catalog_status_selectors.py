from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

def get_default_catalog_status():
    return CatalogStatusProfile.objects.filter(is_default=True).first()
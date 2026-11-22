from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile

def get_published_catalogs():
    return CoreCatalogProfile.objects.filter(is_published=True)
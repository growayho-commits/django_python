from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

def get_primary_medias():
    return CatalogMediaProfile.objects.filter(is_primary=True)
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaSelector:
    @staticmethod
    def get_media_by_catalog(catalog_id: str) -> CatalogMediaProfile | None:
        return CatalogMediaProfile.objects.filter(catalog_id=catalog_id).first()

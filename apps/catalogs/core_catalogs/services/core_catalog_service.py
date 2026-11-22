from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile

class CoreCatalogApplicationService:
    @staticmethod
    def get_all_catalogs():
        return CoreCatalogProfile.objects.all()

    @staticmethod
    def create_catalog(validated_data):
        return CoreCatalogProfile.objects.create(**validated_data)
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusApplicationService:
    @staticmethod
    def get_all_statuses():
        return CatalogStatusProfile.objects.all()

    @staticmethod
    def create_status(validated_data):
        return CatalogStatusProfile.objects.create(**validated_data)
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaApplicationService:
    @staticmethod
    def get_all_medias():
        return CatalogMediaProfile.objects.all()

    @staticmethod
    def create_media(validated_data):
        return CatalogMediaProfile.objects.create(**validated_data)
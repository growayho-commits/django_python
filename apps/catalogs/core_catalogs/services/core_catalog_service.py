from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.selectors.core_catalog_selectors import CoreCatalogSelector


class CoreCatalogApplicationService:
    """Application service handling catalogue creation and role-scoped retrieval."""

    @staticmethod
    def get_all_catalogs():
        return CoreCatalogSelector.get_all_catalogues()

    @staticmethod
    def create_catalog(validated_data, owner=None):
        if owner is not None and "owner" not in validated_data:
            validated_data["owner"] = owner
        return CoreCatalogProfile.objects.create(**validated_data)
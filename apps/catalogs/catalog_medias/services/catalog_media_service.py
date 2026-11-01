from django.db import transaction
from apps.catalogs.catalog_medias.dtos.catalog_media_dtos import CatalogMediaCreateDTO
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogMediaApplicationService:
    @staticmethod
    @transaction.atomic
    def save_media_suite(dto: CatalogMediaCreateDTO) -> CatalogMediaProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        return CatalogMediaProfile.create_or_update_media(catalog_obj=catalog, dto=dto)

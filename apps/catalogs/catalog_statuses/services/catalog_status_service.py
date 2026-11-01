from django.db import transaction
from apps.catalogs.catalog_statuses.dtos.catalog_status_dtos import CatalogStatusUpdateDTO
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogStatusApplicationService:
    @staticmethod
    @transaction.atomic
    def update_catalog_status(dto: CatalogStatusUpdateDTO) -> CatalogStatusProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        return CatalogStatusProfile.update_state(catalog_obj=catalog, dto=dto)

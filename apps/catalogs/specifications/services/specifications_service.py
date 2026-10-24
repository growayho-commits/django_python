from django.db import transaction
from apps.catalogs.specifications.dtos.specifications_dtos import SpecificationsCreateDTO
from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class SpecificationsApplicationService:
    @staticmethod
    @transaction.atomic
    def save_specifications(dto: SpecificationsCreateDTO) -> SpecificationsProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        return SpecificationsProfile.save_specifications(catalog_obj=catalog, dto=dto)

from django.db import transaction
from apps.catalogs.bundles_kits.dtos.bundles_kits_dtos import BundleKitCreateDTO
from apps.catalogs.bundles_kits.models.bundles_kits_profile import BundlesKitsProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class BundlesKitsApplicationService:
    @staticmethod
    @transaction.atomic
    def add_item_to_bundle(dto: BundleKitCreateDTO) -> BundlesKitsProfile:
        parent = CoreCatalog.objects.get(id=dto.parent_bundle_catalog_id)
        child = CoreCatalog.objects.get(id=dto.child_catalog_id)
        return BundlesKitsProfile.add_to_bundle(parent_catalog=parent, child_catalog=child, quantity=dto.quantity_in_bundle)

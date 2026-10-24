from django.db import transaction
from apps.catalogs.pricing_tiers.dtos.pricing_dtos import PricingProfileCreateDTO
from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class PricingApplicationService:
    @staticmethod
    @transaction.atomic
    def create_or_update_pricing(dto: PricingProfileCreateDTO) -> PricingProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        pricing_obj, _ = PricingProfile.objects.update_or_create(
            catalog=catalog,
            defaults={
                'base_price': dto.base_price,
                'mrp_price': dto.mrp_price,
                'tier_1_min_qty': dto.tier_1_min_qty,
                'tier_1_price': dto.tier_1_price,
                'tier_2_min_qty': dto.tier_2_min_qty,
                'tier_2_price': dto.tier_2_price,
                'tier_3_min_qty': dto.tier_3_min_qty,
                'tier_3_price': dto.tier_3_price,
            }
        )
        return pricing_obj

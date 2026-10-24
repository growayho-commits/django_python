import uuid
from django.db import models

class PricingProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField(
        'core_catalogs.CoreCard' if False else 'core_catalogs.CoreCatalog', 
        on_delete=models.CASCADE, 
        related_name='pricing_profile'
    )
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    mrp_price = models.DecimalField(max_digits=12, decimal_places=2)
    tier_1_min_qty = models.PositiveIntegerField(default=1)
    tier_1_price = models.DecimalField(max_digits=12, decimal_places=2)
    tier_2_min_qty = models.PositiveIntegerField(default=10)
    tier_2_price = models.DecimalField(max_digits=12, decimal_places=2)
    tier_3_min_qty = models.PositiveIntegerField(default=100)
    tier_3_price = models.DecimalField(max_digits=12, decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_pricing_profile'

    @classmethod
    def create_pricing(cls, catalog_obj, dto) -> 'PricingProfile':
        if dto.base_price > dto.mrp_price:
            raise ValueError("Domain Rule Violation: Base price cannot be greater than MRP price.")
        return cls(
            catalog=catalog_obj,
            base_price=dto.base_price,
            mrp_price=dto.mrp_price,
            tier_1_min_qty=dto.tier_1_min_qty,
            tier_1_price=dto.tier_1_price,
            tier_2_min_qty=dto.tier_2_min_qty,
            tier_2_price=dto.tier_2_price,
            tier_3_min_qty=dto.tier_3_min_qty,
            tier_3_price=dto.tier_3_price
        )

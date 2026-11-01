# apps/catalogs/pricing_tiers/models/pricing_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class PricingProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='pricing_tiers')
    tier_name = models.CharField(max_length=100)  # எ.கா: Retail, B2B Bulk, Wholesale
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    bulk_min_qty = models.PositiveIntegerField(default=1)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.catalog.name} - {self.tier_name}: {self.base_price}"
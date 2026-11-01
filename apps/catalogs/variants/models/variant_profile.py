# apps/catalogs/variants/models/variant_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogVariantProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='variants')
    variant_name = models.CharField(max_length=150) # எ.கா: Red / XL, 128GB / Black
    sku = models.CharField(max_length=100, unique=True)
    price_override = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True) # தனித்துவமான விலை (தேவைப்பட்டால்)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Variant: {self.variant_name} ({self.sku})"
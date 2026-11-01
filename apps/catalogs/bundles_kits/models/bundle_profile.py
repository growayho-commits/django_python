# apps/catalogs/bundles_kits/models/bundle_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class BundleProfile(models.Model):
    bundle_name = models.CharField(max_length=150) # எ.கா: Summer Combo Pack
    description = models.TextField(blank=True, null=True)
    items = models.ManyToManyField(CoreCatalog, related_name='bundles')
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Bundle: {self.bundle_name} - {self.bundle_price}"
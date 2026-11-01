# apps/catalogs/inventories/models/inventory_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class InventoryProfile(models.Model):
    catalog = models.OneToOneField(CoreCatalog, on_delete=models.CASCADE, related_name='inventory')
    stock_quantity = models.PositiveIntegerField(default=0)
    warehouse_location = models.CharField(max_length=100, blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    last_synced_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.catalog.name} - Stock: {self.stock_quantity}"
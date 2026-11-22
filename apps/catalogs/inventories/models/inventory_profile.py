from django.conf import settings
from django.db import models


class InventoryProfile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='inventories',
        blank=True,
        null=True,
    )
    product = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='inventories',
        blank=True,
        null=True,
    )
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=5)
    warehouse_location = models.CharField(max_length=255, blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.is_in_stock = self.stock_quantity > 0
        super().save(*args, **kwargs)

    @property
    def is_low_stock(self):
        return 0 < self.stock_quantity <= self.low_stock_threshold

    def __str__(self):
        return f"Inventory ({self.sku}) - Qty: {self.stock_quantity}"
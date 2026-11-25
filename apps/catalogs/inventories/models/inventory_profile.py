from django.conf import settings
from django.db import models


class InventoryProfile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='catalogue_inventories',
        null=True,
        blank=True,
    )
    catalogue = models.OneToOneField(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='inventory',
        null=True,
        blank=True,
    )
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    warehouse_location = models.CharField(max_length=255, blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def available_quantity(self) -> int:
        return max(0, self.stock_quantity - self.reserved_quantity)

    @property
    def is_low_stock(self) -> bool:
        return self.available_quantity <= self.low_stock_threshold

    def save(self, *args, **kwargs):
        self.is_in_stock = self.available_quantity > 0
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Inventory ({self.sku}) - Available: {self.available_quantity}"
import uuid
from django.db import models

class InventoryProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.OneToOneField(
        'core_catalogs.CoreCatalog', 
        on_delete=models.CASCADE, 
        related_name='inventory_profile'
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    warehouse_location = models.CharField(max_length=100, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_inventory_profile'

    @classmethod
    def update_stock(cls, catalog_obj, qty: int, threshold: int, location: str) -> 'InventoryProfile':
        if qty < 0:
            raise ValueError("Domain Rule Error: Stock quantity cannot be negative.")
        obj, _ = cls.objects.update_or_create(
            catalog=catalog_obj,
            defaults={
                'stock_quantity': qty,
                'low_stock_threshold': threshold,
                'warehouse_location': location
            }
        )
        return obj

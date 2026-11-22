from django.db import models

class CatalogVariantProfile(models.Model):
    variant_name = models.CharField(max_length=255, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'variants'
        db_table = 'variant_profile'

    def __str__(self):
        return f"{self.variant_name} ({self.sku})"
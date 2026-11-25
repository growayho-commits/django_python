from django.db import models


class CatalogVariantProfile(models.Model):
    catalogue = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='variants',
        null=True,
        blank=True,
    )
    variant_name = models.CharField(max_length=150)
    sku = models.CharField(max_length=100, unique=True)
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        help_text="Added to or subtracted from catalogue base price.",
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.variant_name} ({self.sku})"
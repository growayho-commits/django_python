from django.conf import settings
from django.db import models


class CoreCatalogProfile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='catalog_products',
        blank=True,
        null=True,
    )
    category = models.ForeignKey(
        'categories.CategoryProfile',
        on_delete=models.SET_NULL,
        related_name='products',
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    class UnitChoices(models.TextChoices):
        PIECE = 'pc', 'Piece'
        UNIT = 'unit', 'Unit'
        BOX = 'box', 'Box'

    unit = models.CharField(
        max_length=50,
        choices=UnitChoices.choices,
        default=UnitChoices.UNIT,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.unit})"
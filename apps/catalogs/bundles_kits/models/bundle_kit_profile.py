from django.conf import settings
from django.db import models


class BundleKitProfile(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="catalogue_bundles",
        null=True,
        blank=True,
    )
    bundle_name = models.CharField(max_length=255, unique=True)
    bundle_sku = models.CharField(max_length=100, unique=True)
    catalogues = models.ManyToManyField(
        "core_catalogs.CoreCatalogProfile",
        related_name="bundles",
        blank=True,
    )
    description = models.TextField(blank=True, default="")
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bundle_name} ({self.bundle_sku})"
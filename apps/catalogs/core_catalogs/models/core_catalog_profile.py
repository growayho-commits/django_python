# apps/catalogs/core_catalogs/models/core_catalog_profile.py

from django.db import models

class CoreCatalog(models.Model):
    name = models.CharField(max_length=255, unique=True)
    sku = models.CharField(max_length=100, unique=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"
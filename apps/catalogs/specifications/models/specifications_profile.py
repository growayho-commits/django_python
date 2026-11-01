# apps/catalogs/specifications/models/specifications_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class SpecificationsProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='specifications')
    spec_key = models.CharField(max_length=100)   # எ.கா: Weight, Dimensions, Compatibility
    spec_value = models.TextField()               # எ.கா: 1.5 kg, 10x20 cm, Machine Model X
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.catalog.name} - {self.spec_key}: {self.spec_value}"
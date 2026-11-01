# apps/catalogs/attributes/models/attribute_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class AttributeProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.CharField(max_length=100)  # எ.கா: Color, Size, GSM
    attribute_value = models.CharField(max_length=255) # எ.கா: Blue, XL, 180GSM
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.catalog.name} - {self.attribute_name}: {self.attribute_value}"
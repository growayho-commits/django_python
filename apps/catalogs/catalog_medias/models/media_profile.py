# apps/catalogs/catalog_medias/models/media_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogMediaProfile(models.Model):
    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='media_files')
    image = models.ImageField(upload_to='catalogs/images/', blank=True, null=True)
    alt_text = models.CharField(max_length=150, blank=True, null=True)
    is_primary = models.BooleanField(default=False) # முதன்மைப் படமா என்பதைத் தீர்மானிக்க
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Media for {self.catalog.name} (Primary: {self.is_primary})"
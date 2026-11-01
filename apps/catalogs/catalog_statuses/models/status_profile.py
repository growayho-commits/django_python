# apps/catalogs/catalog_statuses/models/status_profile.py

from django.db import models
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CatalogStatusProfile(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('pending_approval', 'Pending Approval'),
        ('active', 'Active'),
        ('out_of_stock', 'Out of Stock'),
        ('archived', 'Archived'),
    )

    catalog = models.ForeignKey(CoreCatalog, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='draft')
    remarks = models.TextField(blank=True, null=True) # நிலை மாற்றத்திற்கான காரணங்கள் அல்லது குறிப்புகள்
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.catalog.name} - Status: {self.get_status_display()}"
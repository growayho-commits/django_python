import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class AttributeProfile(models.Model):
    """
    Manages dynamic attributes (Material, GSM, Voltage, etc.) mapped to catalogs.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.ForeignKey(
        'core_catalog.CoreCatalog', 
        on_delete=models.CASCADE, 
        related_name='attributes'
    )
    attribute_name = models.CharField(max_length=100, help_text="e.g. Material, GSM, Voltage[cite: 1]")
    attribute_value = models.CharField(max_length=255, help_text="e.g. Stainless Steel 304, 180 GSM[cite: 1]")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_attribute_profile'
        verbose_name = _('Attribute Profile')
        verbose_name_plural = _('Attribute Profiles')

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value} for {self.catalog.title}"
[cite: 1]
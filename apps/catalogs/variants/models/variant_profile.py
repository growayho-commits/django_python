import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _

class VariantProfile(models.Model):
    """
    Manages individual SKUs created by attribute combinations (e.g., Size: XL + Color: Blue)[cite: 1].
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog = models.ForeignKey(
        'core_catalog.CoreCatalog', 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    variant_sku = models.CharField(max_length=100, unique=True, help_text="Unique SKU for this variant[cite: 1]")
    size_variation = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. 1200mm, XL[cite: 1]")
    color_variation = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Matte Blue[cite: 1]")
    additional_price_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Price difference for this variant")
    
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_variant_profile'
        verbose_name = _('Variant Profile')
        verbose_name_plural = _('Variant Profiles')

    def __str__(self):
        return f"Variant {self.variant_sku} - {self.catalog.title}"
[cite: 1]
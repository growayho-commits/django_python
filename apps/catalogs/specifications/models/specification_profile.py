from django.db import models


class SpecificationProfile(models.Model):
    catalogue = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='specifications',
        null=True,
        blank=True,
    )
    spec_group = models.CharField(max_length=100, default='General')
    spec_key = models.CharField(max_length=120, default='')
    spec_value = models.CharField(max_length=255)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', 'spec_group', 'spec_key']

    def __str__(self):
        return f"{self.spec_group} | {self.spec_key}: {self.spec_value}"
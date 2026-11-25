from django.db import models


class CatalogMediaProfile(models.Model):
    class MediaTypeChoices(models.TextChoices):
        IMAGE = 'image', 'Image'
        VIDEO = 'video', 'Video'
        BROCHURE = 'brochure', 'PDF Brochure'

    catalogue = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.CASCADE,
        related_name='medias',
        null=True,
        blank=True,
    )
    media_type = models.CharField(max_length=20, choices=MediaTypeChoices.choices, default=MediaTypeChoices.IMAGE)
    media_url = models.URLField(max_length=500, blank=True, null=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    display_order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['display_order', '-is_primary']

    def __str__(self):
        return f"{self.media_type.title()} - {self.catalogue.name if self.catalogue else 'Unlinked'}"
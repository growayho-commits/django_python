from django.db import models

class CatalogMediaProfile(models.Model):
    title = models.CharField(max_length=255)
    media_url = models.URLField(max_length=500)
    media_type = models.CharField(max_length=50, default='image') # image, video, document
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.media_type})"
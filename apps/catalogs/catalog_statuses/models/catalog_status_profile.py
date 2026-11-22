from django.db import models

class CatalogStatusProfile(models.Model):
    status_name = models.CharField(max_length=100, unique=True)
    status_code = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.status_name
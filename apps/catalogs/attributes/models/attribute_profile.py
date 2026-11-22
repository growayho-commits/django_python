from django.db import models

class AttributeProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(max_length=255, unique=True)
    data_type = models.CharField(max_length=50, default='string') # string, integer, boolean
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
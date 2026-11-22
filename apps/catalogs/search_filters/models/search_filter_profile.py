from django.db import models

class SearchFilterProfile(models.Model):
    filter_name = models.CharField(max_length=255, unique=True)
    filter_key = models.SlugField(max_length=255, unique=True)
    filter_type = models.CharField(max_length=50, default='checkbox') # checkbox, range, dropdown
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filter_name
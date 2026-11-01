# apps/catalogs/search_filters/models/filter_profile.py

from django.db import models
from apps.catalogs.categories.models.category_profile import CategoryProfile

class SearchFilterProfile(models.Model):
    category = models.ForeignKey(CategoryProfile, on_delete=models.CASCADE, related_name='search_filters')
    filter_name = models.CharField(max_length=100) # எ.கா: Brand, Color, RAM Size
    filter_key = models.CharField(max_length=100)  # எ.கா: brand, color, ram_size
    filter_options = models.JSONField(default=list) # தேர்ந்தெடுக்கக்கூடிய தேர்வுகள் (எ.கா: ["Apple", "Samsung", "Sony"])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Filter: {self.filter_name} for {self.category.name}"
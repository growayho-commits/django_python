# apps/catalogs/categories/serializers/category_profile.py

from rest_framework import serializers
from apps.catalogs.categories.models.category_profile import CategoryProfile  # அல்லது உங்கள் கேட்டகிரி மாடல் பெயர்

class CategoryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProfile
        fields = ['id', 'name', 'slug', 'parent', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
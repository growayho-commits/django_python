from rest_framework import serializers
from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryProfile
        fields = ['id', 'name', 'slug', 'description', 'is_active', 'created_at', 'updated_at']
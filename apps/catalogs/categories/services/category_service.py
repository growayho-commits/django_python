# apps/catalogs/categories/services/category_service.py

from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategoryService:
    @staticmethod
    def create_category(validated_data):
        """புதிய கேட்டகிரியைச் சேர்க்க (Add)"""
        return CategoryProfile.objects.create(**validated_data)

    @staticmethod
    def update_category(category_id, validated_data):
        """கேட்டகிரி விவரங்களைப் புதுப்பிக்க (Edit / Update)"""
        try:
            category = CategoryProfile.objects.get(id=category_id)
            for key, value in validated_data.items():
                setattr(category, key, value)
            category.save()
            return category
        except CategoryProfile.DoesNotExist:
            raise ValueError("Category profile does not exist.")
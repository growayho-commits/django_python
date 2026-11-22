from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategoryApplicationService:
    @staticmethod
    def get_all_categories():
        return CategoryProfile.objects.all()

    @staticmethod
    def create_category(validated_data):
        return CategoryProfile.objects.create(**validated_data)

    @staticmethod
    def update_category(category_id, validated_data):
        category = CategoryProfile.objects.get(id=category_id)
        for attr, value in validated_data.items():
            setattr(category, attr, value)
        category.save()
        return category
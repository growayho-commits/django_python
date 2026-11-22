from apps.catalogs.categories.models.category_profile import CategoryProfile

def get_active_categories():
    return CategoryProfile.objects.filter(is_active=True)
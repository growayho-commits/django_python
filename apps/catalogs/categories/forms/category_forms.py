from django import forms
from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = CategoryProfile
        fields = ['name', 'slug', 'description', 'is_active']
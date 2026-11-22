from django import forms
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile

class CoreCatalogAdminForm(forms.ModelForm):
    class Meta:
        model = CoreCatalogProfile
        fields = ['title', 'sku', 'description', 'base_price', 'is_published']
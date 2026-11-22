from django import forms
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusAdminForm(forms.ModelForm):
    class Meta:
        model = CatalogStatusProfile
        fields = ['status_name', 'status_code', 'description', 'is_default']
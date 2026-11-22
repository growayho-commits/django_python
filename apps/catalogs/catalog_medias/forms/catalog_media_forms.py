from django import forms
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaAdminForm(forms.ModelForm):
    class Meta:
        model = CatalogMediaProfile
        fields = ['title', 'media_url', 'media_type', 'is_primary']
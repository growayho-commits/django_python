from django import forms
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.validators.core_catalog_validators import validate_unique_catalogue_name


class CoreCatalogForm(forms.ModelForm):
    class Meta:
        model = CoreCatalogProfile
        exclude = ['owner', 'created_at', 'updated_at']
        labels = {
            'name': 'Catalogue Name',
            'description': 'Catalogue Description',
            'unit': 'Catalogue Unit',
            'is_active': 'Active Catalogue',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter unique catalogue name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter catalogue details'}),
        }

    def clean_name(self):
        return validate_unique_catalogue_name(self.cleaned_data.get('name', ''), instance=self.instance)
    
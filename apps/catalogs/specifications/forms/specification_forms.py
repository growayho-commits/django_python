from django import forms
from apps.catalogs.specifications.models.specification_profile import SpecificationProfile

class SpecificationAdminForm(forms.ModelForm):
    class Meta:
        model = SpecificationProfile
        fields = ['title', 'value', 'unit']
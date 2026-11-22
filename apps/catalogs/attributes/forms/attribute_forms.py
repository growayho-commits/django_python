from django import forms
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeAdminForm(forms.ModelForm):
    class Meta:
        model = AttributeProfile
        fields = ['name', 'code', 'data_type', 'is_required']
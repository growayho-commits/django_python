from django import forms
from apps.catalogs.pricing_extras.models.pricing_extra_profile import PricingExtraProfile

class PricingExtraAdminForm(forms.ModelForm):
    class Meta:
        model = PricingExtraProfile
        fields = ['extra_name', 'extra_code', 'additional_fee', 'is_mandatory']
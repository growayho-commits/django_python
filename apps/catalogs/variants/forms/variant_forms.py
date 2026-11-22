from django import forms
from apps.catalogs.variants.models.variant_profile import VariantProfile

class VariantAdminForm(forms.ModelForm):
    class Meta:
        model = VariantProfile
        fields = ['product_name', 'variant_sku', 'color', 'size', 'price_override', 'is_active']
from django import forms
from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile

class PricingTierAdminForm(forms.ModelForm):
    class Meta:
        model = PricingTierProfile
        fields = ['tier_name', 'min_quantity', 'max_quantity', 'discount_percentage', 'is_active']
from django import forms
from apps.catalogs.bundles_kits.models.bundle_kit_profile import BundleKitProfile

class BundleKitAdminForm(forms.ModelForm):
    class Meta:
        model = BundleKitProfile
        fields = ['bundle_name', 'bundle_sku', 'bundle_price', 'is_active']
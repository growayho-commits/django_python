from django import forms
from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile

class CatalogWishlistAdminForm(forms.ModelForm):
    class Meta:
        model = CatalogWishlistProfile
        fields = ['user_identifier', 'product_sku', 'notes']
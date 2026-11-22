from django import forms
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryAdminForm(forms.ModelForm):
    class Meta:
        model = InventoryProfile
        fields = ['sku', 'stock_quantity', 'low_stock_threshold', 'warehouse_location', 'is_in_stock']
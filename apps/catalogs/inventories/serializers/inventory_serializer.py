from rest_framework import serializers
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProfile
        fields = ['id', 'sku', 'stock_quantity', 'low_stock_threshold', 'warehouse_location', 'is_in_stock', 'created_at', 'updated_at']
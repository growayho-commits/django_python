# apps/catalogs/inventories/serializers/inventory_serializer.py

from rest_framework import serializers
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProfile
        fields = ['id', 'catalog', 'stock_quantity', 'warehouse_location', 'is_in_stock', 'last_synced_at']
        read_only_fields = ['id', 'last_synced_at']
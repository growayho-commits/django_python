from rest_framework import serializers
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryProfile
        fields = '__all__'

# apps/catalogs/inventories/services/inventory_service.py

from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryService:
    @staticmethod
    def create_inventory(validated_data):
        """புதிய இருப்புப் பதிவைச் சேர்க்க (Add)"""
        return InventoryProfile.objects.create(**validated_data)

    @staticmethod
    def update_inventory(inventory_id, validated_data):
        """சரக்கு இருப்பைப் புதுப்பிக்க (Edit / Update / Sync)"""
        try:
            inventory = InventoryProfile.objects.get(id=inventory_id)
            for key, value in validated_data.items():
                setattr(inventory, key, value)
            
            # Stock quantity அடிப்படையாக கொண்டு is_in_stock நிலையை மாற்றியமைத்தல்
            if 'stock_quantity' in validated_data:
                inventory.is_in_stock = inventory.stock_quantity > 0
                
            inventory.save()
            return inventory
        except InventoryProfile.DoesNotExist:
            raise ValueError("Inventory profile does not exist.")
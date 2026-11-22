from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryApplicationService:
    @staticmethod
    def get_all_inventories():
        return InventoryProfile.objects.all()

    @staticmethod
    def create_inventory(validated_data):
        return InventoryProfile.objects.create(**validated_data)
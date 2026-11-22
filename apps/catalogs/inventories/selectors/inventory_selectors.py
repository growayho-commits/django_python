from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

def get_out_of_stock_items():
    return InventoryProfile.objects.filter(stock_quantity=0)
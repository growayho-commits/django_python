from dataclasses import dataclass

@dataclass(frozen=True)
class InventoryUpdateDTO:
    catalog_id: str
    stock_quantity: int
    low_stock_threshold: int
    warehouse_location: str

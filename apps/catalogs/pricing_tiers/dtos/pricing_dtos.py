from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class PricingProfileCreateDTO:
    catalog_id: str
    base_price: Decimal
    mrp_price: Decimal
    tier_1_min_qty: int
    tier_1_price: Decimal
    tier_2_min_qty: int
    tier_2_price: Decimal
    tier_3_min_qty: int
    tier_3_price: Decimal

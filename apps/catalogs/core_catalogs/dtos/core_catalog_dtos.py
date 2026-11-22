from dataclasses import dataclass
from decimal import Decimal
from typing import Optional

@dataclass(frozen=True)
class CoreCatalogCreateDTO:
    catalog_code: str
    title: str
    slug: str
    root_category: str
    sub_category: str
    short_description: str
    long_description: str
    hsn_or_sac_code: str
    gst_percentage: Decimal
    brand_name: str = "HYBRID MARKETPLACE"
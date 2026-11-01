from dataclasses import dataclass

@dataclass(frozen=True)
class WishlistActionDTO:
    user_id: str
    catalog_id: str

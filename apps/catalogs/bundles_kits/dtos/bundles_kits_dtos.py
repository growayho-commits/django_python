from dataclasses import dataclass

@dataclass(frozen=True)
class BundleKitCreateDTO:
    parent_bundle_catalog_id: str
    child_catalog_id: str
    quantity_in_bundle: int = 1

from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class CatalogStatusUpdateDTO:
    catalog_id: str
    lifecycle_state: str
    verified_by_superuser_id: Optional[str] = None
    approval_rejection_reason: Optional[str] = None

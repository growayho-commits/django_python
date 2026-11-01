from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass(frozen=True)
class SpecificationsCreateDTO:
    catalog_id: str
    dimensions_lwh: str
    weight_kg: float
    material_type: str
    operating_voltage: str
    compatibility_details: str
    technical_spec_sheet: Dict[str, Any] = field(default_factory=dict)

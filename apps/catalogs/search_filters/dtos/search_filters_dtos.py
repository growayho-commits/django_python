from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class SearchFiltersCreateDTO:
    catalog_id: str
    tags: List[str] = field(default_factory=list)
    meta_keywords: List[str] = field(default_factory=list)
    faceted_search_json: dict = field(default_factory=dict)

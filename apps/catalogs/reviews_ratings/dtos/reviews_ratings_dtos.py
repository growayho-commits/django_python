from dataclasses import dataclass, field
from typing import List

@dataclass(frozen=True)
class ReviewCreateDTO:
    catalog_id: str
    user_id: str
    star_rating: int
    review_comment: str
    user_uploaded_images: List[str] = field(default_factory=list)

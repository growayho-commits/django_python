from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class CatalogMediaCreateDTO:
    catalog_id: str
    primary_image_url: str
    gallery_image_urls: List[str] = field(default_factory=list)
    interactive_360_urls: List[str] = field(default_factory=list)
    demo_video_url: Optional[str] = None
    model_3d_gltf_url: Optional[str] = None
    ar_usdz_url: Optional[str] = None
    dxf_drawing_url: Optional[str] = None

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
    brand_name: str = "GROWAY SOLUTIONS"
```[cite: 1, 2]

---

### 2. Domain Model with Business Invariants (`apps/catalogs/core_catalogs/models/core_catalog_profile.py`)
வெறும் டேபிள் அல்லாமல், பிசினஸ் விதிகளைத் தன்வசம் கொண்டுள்ள உண்மையான Domain Entity[cite: 1, 2]:

```python
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.catalogs.core_catalogs.dtos.core_catalog_dtos import CoreCatalogCreateDTO

class CatalogType(models.TextChoices):
    GOODS = 'GOODS', _('Goods (Physical Product)')
    SERVICE = 'SERVICE', _('Service (Execution/Maintenance)')

class CoreCatalog(models.Model):
    """
    True DDD Aggregate Root enforcing business invariants and rules.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    catalog_code = models.CharField(max_length=64, unique=True, db_index=True)
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True)
    
    catalog_type = models.CharField(max_length=16, choices=CatalogType.choices)
    brand_name = models.CharField(max_length=150)
    
    root_category = models.CharField(max_length=150)
    sub_category = models.CharField(max_length=150)
    
    short_description = models.TextField()
    long_description = models.TextField()
    
    hsn_or_sac_code = models.CharField(max_length=20)
    gst_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    
    is_active = models.BooleanField(default=True)
    is_draft = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'catalog_core_catalog'

    @classmethod
    def create_new_catalog(cls, dto: CoreCatalogCreateDTO) -> 'CoreCatalog':
        """
        Domain Business Rule: Automatically determine GOODS vs SERVICE based on HSN/SAC code prefix.
        Enforces domain invariants before persistence.
        """
        if not dto.catalog_code or not dto.title:
            raise ValueError("Catalog Code and Title are mandatory domain invariants.")

        # Business Logic: HSN starting with '99' is Service, else Goods
        if dto.hsn_or_sac_code.startswith('99'):
            catalog_type = CatalogType.SERVICE
        else:
            catalog_type = CatalogType.GOODS

        return cls(
            catalog_code=dto.catalog_code,
            title=dto.title,
            slug=dto.slug,
            catalog_type=catalog_type,
            brand_name=dto.brand_name,
            root_category=dto.root_category,
            sub_category=dto.sub_category,
            short_description=dto.short_description,
            long_description=dto.long_description,
            hsn_or_sac_code=dto.hsn_or_sac_code,
            gst_percentage=dto.gst_percentage,
            is_draft=True
        )
```[cite: 1, 2]

---

### 3. Application Services Layer (`apps/catalogs/core_catalogs/services/core_catalog_service.py`)
டொமைன் லாஜிக்கை ஒருங்கிணைத்து, டேட்டாபேஸ் டிரான்ஸாக்ஷனை மட்டும் கையாளுபவை (Use Case Orchestration)[cite: 1, 2]:

```python
from django.db import transaction
from apps.catalogs.core_catalogs.dtos.core_catalog_dtos import CoreCatalogCreateDTO
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class CoreCatalogApplicationService:
    """
    Application Service (Use Case Layer) - Coordinates Write operations and Domain Events.
    Strictly separates business logic from HTTP and Database details (SoC & DDD).
    """
    @staticmethod
    @transaction.atomic
    def register_new_catalog(dto: CoreCatalogCreateDTO) -> CoreCatalog:
        # Invoke Domain Aggregate Root factory method for business validation
        catalog = CoreCatalog.create_new_catalog(dto)
        
        # Persistence Layer execution
        catalog.save()
        
        # Here domain events/signals can be triggered safely
        return catalog
```[cite: 1, 2]

இந்த முறைப்படி ஒவ்வொரு ஆப்பிலும் DTOs, Domain Model Invariants மற்றும் Application Services-ஐப் பின்பற்றும் போது முழுமையான **Domain-Driven Design (DDD)** மற்றும் **Separation of Concerns (SoC)** முறை சாத்தியமாகிறது[cite: 1, 2]. இதை மற்ற சப்-ஆப்களுக்கும் விரிவுபடுத்தலாமா?
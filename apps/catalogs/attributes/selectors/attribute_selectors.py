from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeSelector:
    """
    Read-only operations for Catalog Attributes adhering to CQRS principles[cite: 1].
    """
    @staticmethod
    def get_attributes_by_catalog(catalog_id: str):
        return AttributeProfile.objects.filter(catalog_id=catalog_id)

    @staticmethod
    def get_attribute_by_id(attribute_id: str):
        return AttributeProfile.objects.filter(id=attribute_id).first()
```[cite: 1]

---

### 2. Variants Selector (`apps/catalogs/variants/selectors/variant_selectors.py`)
```python
from apps.catalogs.variants.models.variant_profile import VariantProfile

class VariantSelector:
    """
    Read-only operations for Catalog Variants (Size, Color Matrix)[cite: 1].
    """
    @staticmethod
    def get_variants_by_catalog(catalog_id: str):
        return VariantProfile.objects.filter(catalog_id=catalog_id, is_available=True)

    @staticmethod
    def get_variant_by_sku(variant_sku: str):
        return VariantProfile.objects.filter(variant_sku=variant_sku, is_available=True).first()
```[cite: 1]

---

### 3. Catalog Media Selector (`apps/catalogs/catalog_medias/selectors/catalog_media_selectors.py`)
```python
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaSelector:
    """
    Read-only operations for Rich Media, 3D AR Assets, and CAD files[cite: 1].
    """
    @staticmethod
    def get_media_by_catalog(catalog_id: str):
        return CatalogMediaProfile.objects.filter(catalog_id=catalog_id).first()
```[cite: 1]

---

### 4. Pricing Tiers Selector (`apps/catalogs/pricing_tiers/selectors/pricing_selectors.py`)
```python
from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingSelector:
    """
    Read-only operations for Base Price, MRP, and B2B Wholesale Tiers[cite: 1].
    """
    @staticmethod
    def get_pricing_by_catalog(catalog_id: str):
        return PricingProfile.objects.filter(catalog_id=catalog_id).first()
```[cite: 1]

---

### 5. Inventory Selector (`apps/catalogs/inventories/selectors/inventory_selectors.py`)
```python
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventorySelector:
    """
    Read-only operations for Stock Levels and Inventory status[cite: 1].
    """
    @staticmethod
    def get_inventory_by_catalog(catalog_id: str):
        return InventoryProfile.objects.filter(catalog_id=catalog_id).first()
```[cite: 1]

---

இந்த செலக்டர்கள் அனைத்தும் டேட்டாபேஸிலிருந்து பாதுகாப்பாகத் தரவுகளைப் படிக்க (Read/Fetch) மட்டும் உதவும் வகையில் உருவாக்கப்பட்டுள்ளன[cite: 1]. அடுத்ததாக **Specifications, Bundles, Wishlists மற்றும் Reviews** ஆப்களுக்கான Selectors கோடுகளை உருவாக்கலாமா?
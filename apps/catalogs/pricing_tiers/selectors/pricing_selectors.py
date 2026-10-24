from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingSelector:
    """
    CQRS Read Operations for Pricing and B2B Tiers[cite: 1, 2].
    """
    @staticmethod
    def get_pricing_by_catalog(catalog_id: str) -> PricingProfile | None:
        return PricingProfile.objects.filter(catalog_id=catalog_id).first()

    @staticmethod
    def get_wholesale_price_for_quantity(catalog_id: str, quantity: int):
        pricing = PricingProfile.objects.filter(catalog_id=catalog_id).first()
        if not pricing:
            return None
        
        # Domain read logic to determine applicable tier
        if quantity >= pricing.tier_3_min_qty:
            return pricing.tier_3_price
        elif quantity >= pricing.tier_2_min_qty:
            return pricing.tier_2_price
        return pricing.tier_1_price
```[cite: 1, 2]

---

### 2. Inventory Selector (`apps/catalogs/inventories/selectors/inventory_selectors.py`)
பொருட்கள் மற்றும் சேவைகளின் இருப்பு நிலையைச் சரிபார்க்கும் செலக்டர்[cite: 1, 2]:

```python
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventorySelector:
    """
    CQRS Read Operations for Inventory stock levels[cite: 1, 2].
    """
    @staticmethod
    def get_inventory_by_catalog(catalog_id: str) -> InventoryProfile | None:
        return InventoryProfile.objects.filter(catalog_id=catalog_id).first()

    @staticmethod
    def check_stock_availability(catalog_id: str, required_qty: int) -> bool:
        inventory = InventoryProfile.objects.filter(catalog_id=catalog_id).first()
        if not inventory:
            return False
        return inventory.is_in_stock and inventory.stock_quantity >= required_qty
```[cite: 1, 2]

---

### 3. Categories Selector (`apps/catalogs/categories/selectors/category_selectors.py`)
உலகளாவிய தரப்படுத்தப்பட்ட வகைப்பாடு மரத்தைக் (Global Master Category Tree) கையாளும் செலக்டர்[cite: 1, 2]:

```python
from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategorySelector:
    """
    CQRS Read Operations for Global Category Tree[cite: 1, 2].
    """
    @staticmethod
    def get_root_categories():
        return CategoryProfile.objects.filter(parent__isnull=True, is_active=True)

    @staticmethod
    def get_subcategories(parent_category_id: str):
        return CategoryProfile.objects.filter(parent_id=parent_category_id, is_active=True)

    @staticmethod
    def get_category_by_slug(slug: str) -> CategoryProfile | None:
        return CategoryProfile.objects.filter(slug=slug, is_active=True).first()
```[cite: 1, 2]

---

இந்த செலக்டர்கள் அனைத்தும் பிசினஸ் லாஜிக்குகளை மாற்றாமல், டேட்டாவை மட்டும் திறம்படப் படிக்க (Read/Fetch) உதவுகின்றன[cite: 1, 2]. அடுத்து **Serializers மற்றும் Views** அடுக்குகளைத் தொடங்கலாமா?
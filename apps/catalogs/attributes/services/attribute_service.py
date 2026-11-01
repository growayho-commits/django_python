from django.db import transaction
from apps.catalogs.attributes.models.attribute_profile import AttributeProfile

class AttributeService:
    @staticmethod
    @transaction.atomic
    def create_attribute(validated_data: dict) -> AttributeProfile:
        return AttributeProfile.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_attribute(attribute_id: str, validated_data: dict) -> AttributeProfile:
        attribute = AttributeProfile.objects.get(id=attribute_id)
        for attr, value in validated_data.items():
            setattr(attribute, attr, value)
        attribute.save()
        return attribute
```[cite: 1, 2]

---

### 2. Variants Service (`apps/catalogs/variants/services/variant_service.py`)
```python
from django.db import transaction
from apps.catalogs.variants.models.variant_profile import VariantProfile

class VariantService:
    @staticmethod
    @transaction.atomic
    def create_variant(validated_data: dict) -> VariantProfile:
        return VariantProfile.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_variant(variant_id: str, validated_data: dict) -> VariantProfile:
        variant = VariantProfile.objects.get(id=variant_id)
        for attr, value in validated_data.items():
            setattr(variant, attr, value)
        variant.save()
        return variant
```[cite: 1, 2]

---

### 3. Catalog Media Service (`apps/catalogs/catalog_medias/services/catalog_media_service.py`)
```python
from django.db import transaction
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile

class CatalogMediaService:
    @staticmethod
    @transaction.atomic
    def save_media_suite(catalog_id: str, validated_data: dict) -> CatalogMediaProfile:
        media_obj, created = CatalogMediaProfile.objects.update_or_create(
            catalog_id=catalog_id,
            defaults=validated_data
        )
        return media_obj
```[cite: 1, 2]

---

### 4. Pricing Tiers Service (`apps/catalogs/pricing_tiers/services/pricing_service.py`)
```python
from django.db import transaction
from apps.catalogs.pricing_tiers.models.pricing_profile import PricingProfile

class PricingService:
    @staticmethod
    @transaction.atomic
    def save_pricing_profile(catalog_id: str, validated_data: dict) -> PricingProfile:
        pricing_obj, created = PricingProfile.objects.update_or_create(
            catalog_id=catalog_id,
            defaults=validated_data
        )
        return pricing_obj
```[cite: 1, 2]

---

### 5. Inventory Service (`apps/catalogs/inventories/services/inventory_service.py`)
```python
from django.db import transaction
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile

class InventoryService:
    @staticmethod
    @transaction.atomic
    def update_stock(catalog_id: str, quantity: int) -> InventoryProfile:
        inventory_obj, created = InventoryProfile.objects.get_or_create(catalog_id=catalog_id)
        inventory_obj.stock_quantity = quantity
        inventory_obj.is_in_stock = quantity > 0
        inventory_obj.save()
        return inventory_obj
```[cite: 1, 2]

---

### 6. Specifications Service (`apps/catalogs/specifications/services/specifications_service.py`)
```python
from django.db import transaction
from apps.catalogs.specifications.models.specifications_profile import SpecificationsProfile

class SpecificationsService:
    @staticmethod
    @transaction.atomic
    def save_specifications(catalog_id: str, validated_data: dict) -> SpecificationsProfile:
        spec_obj, created = SpecificationsProfile.objects.update_or_create(
            catalog_id=catalog_id,
            defaults=validated_data
        )
        return spec_obj
```[cite: 1, 2]

---

### 7. Bundles & Kits Service (`apps/catalogs/bundles_kits/services/bundles_kits_service.py`)
```python
from django.db import transaction
from apps.catalogs.bundles_kits.models.bundles_kits_profile import BundlesKitsProfile

class BundlesKitsService:
    @staticmethod
    @transaction.atomic
    def add_catalog_to_bundle(parent_id: str, child_id: str, quantity: int) -> BundlesKitsProfile:
        bundle_obj, created = BundlesKitsProfile.objects.update_or_create(
            parent_bundle_catalog_id=parent_id,
            child_catalog_id=child_id,
            defaults={'quantity_in_bundle': quantity}
        )
        return bundle_obj
```[cite: 1, 2]

---

### 8. Search & Filters Service (`apps/catalogs/search_filters/services/search_filters_service.py`)
```python
from django.db import transaction
from apps.catalogs.search_filters.models.search_filters_profile import SearchFiltersProfile

class SearchFiltersService:
    @staticmethod
    @transaction.atomic
    def save_search_filters(catalog_id: str, validated_data: dict) -> SearchFiltersProfile:
        filter_obj, created = SearchFiltersProfile.objects.update_or_create(
            catalog_id=catalog_id,
            defaults=validated_data
        )
        return filter_obj
```[cite: 1, 2]

---

### 9. Wishlists Service (`apps/catalogs/wishlists/services/wishlists_service.py`)
```python
from django.db import transaction
from apps.catalogs.wishlists.models.wishlists_profile import WishlistProfile

class WishlistService:
    @staticmethod
    @transaction.atomic
    def add_to_wishlist(user_id: str, catalog_id: str) -> WishlistProfile:
        wishlist_obj, created = WishlistProfile.objects.get_or_create(
            user_id=user_id,
            catalog_id=catalog_id
        )
        return wishlist_obj

    @staticmethod
    @transaction.atomic
    def remove_from_wishlist(user_id: str, catalog_id: str) -> bool:
        deleted_count, _ = WishlistProfile.objects.filter(user_id=user_id, catalog_id=catalog_id).delete()
        return deleted_count > 0
```[cite: 1, 2]

---

### 10. Reviews & Ratings Service (`apps/catalogs/reviews_ratings/services/reviews_ratings_service.py`)
```python
from django.db import transaction
from apps.catalogs.reviews_ratings.models.reviews_ratings_profile import ReviewsRatingsProfile

class ReviewsRatingsService:
    @staticmethod
    @transaction.atomic
    def create_review(validated_data: dict) -> ReviewsRatingsProfile:
        return ReviewsRatingsProfile.objects.create(**validated_data)
```[cite: 1, 2]

---

### 11. Catalog Status Service (`apps/catalogs/catalog_statuses/services/catalog_status_service.py`)
```python
from django.db import transaction
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile

class CatalogStatusService:
    @staticmethod
    @transaction.atomic
    def update_lifecycle_state(catalog_id: str, new_state: str, superuser_id=None, reason=None) -> CatalogStatusProfile:
        status_obj, created = CatalogStatusProfile.objects.get_or_create(catalog_id=catalog_id)
        status_obj.lifecycle_state = new_state
        if superuser_id:
            status_obj.verified_by_superuser_id = superuser_id
        if reason:
            status_obj.approval_rejection_reason = reason
        status_obj.save()
        return status_obj
```[cite: 1, 2]

---

### 12. Categories Service (`apps/catalogs/categories/services/category_service.py`)
```python
from django.db import transaction
from apps.catalogs.categories.models.category_profile import CategoryProfile

class CategoryService:
    @staticmethod
    @transaction.atomic
    def create_category(validated_data: dict) -> CategoryProfile:
        return CategoryProfile.objects.create(**validated_data)
```[cite: 1, 2]

---

### 13. Core Catalogs Service (`apps/catalogs/core_catalogs/services/core_catalog_service.py`)
```python
from django.db import transaction
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog, CatalogType

class CoreCatalogService:
    @staticmethod
    @transaction.atomic
    def create_core_catalog(validated_data: dict) -> CoreCatalog:
        code = validated_data.get('hsn_or_sac_code', '')
        if code.startswith('99'):
            catalog_type = CatalogType.SERVICE
        else:
            catalog_type = CatalogType.GOODS

        validated_data['catalog_type'] = catalog_type
        return CoreCatalog.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_core_catalog(catalog_id: str, validated_data: dict) -> CoreCatalog:
        catalog = CoreCatalog.objects.get(id=catalog_id)
        for attr, value in validated_data.items():
            setattr(catalog, attr, value)
        catalog.save()
        return catalog
```[cite: 1, 2]
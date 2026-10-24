from django.db import transaction
from apps.catalogs.wishlists.dtos.wishlists_dtos import WishlistActionDTO
from apps.catalogs.wishlists.models.wishlists_profile import WishlistProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class WishlistApplicationService:
    @staticmethod
    @transaction.atomic
    def add_to_wishlist(dto: WishlistActionDTO) -> WishlistProfile:
        catalog = CoreCatalog.objects.get(id=dto.catalog_id)
        obj, _ = WishlistProfile.objects.get_or_create(user_id=dto.user_id, catalog=catalog)
        return obj

    @staticmethod
    @transaction.atomic
    def remove_from_wishlist(dto: WishlistActionDTO) -> bool:
        deleted_count, _ = WishlistProfile.objects.filter(user_id=dto.user_id, catalog_id=dto.catalog_id).delete()
        return deleted_count > 0

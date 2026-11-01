# apps/marketing_leads/wishlists/services/wishlists_service.py

from ..models.wishlists_profile import WishlistProfile

class WishlistService:
    @staticmethod
    def add_to_wishlist(user, product_id):
        wishlist_item, created = WishlistProfile.objects.get_or_create(
            user=user, product_id=product_id
        )
        return wishlist_item, created

    @staticmethod
    def remove_from_wishlist(user, product_id):
        count, _ = WishlistProfile.objects.filter(user=user, product_id=product_id).delete()
        return count > 0
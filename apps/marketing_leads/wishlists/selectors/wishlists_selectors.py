from apps.catalogs.wishlists.models.wishlists_profile import WishlistProfile

class WishlistSelector:
    @staticmethod
    def get_user_wishlist(user_id: str):
        return WishlistProfile.objects.filter(user_id=user_id)

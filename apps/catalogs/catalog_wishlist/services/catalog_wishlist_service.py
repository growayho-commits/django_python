from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile

class CatalogWishlistApplicationService:
    @staticmethod
    def get_all_wishlists():
        return CatalogWishlistProfile.objects.all()

    @staticmethod
    def create_wishlist_item(validated_data):
        return CatalogWishlistProfile.objects.create(**validated_data)
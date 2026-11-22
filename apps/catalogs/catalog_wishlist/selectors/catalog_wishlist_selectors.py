from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile

def get_user_wishlist(user_id):
    return CatalogWishlistProfile.objects.filter(user_identifier=user_id)
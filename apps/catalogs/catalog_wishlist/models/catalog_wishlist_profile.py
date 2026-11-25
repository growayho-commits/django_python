from django.conf import settings
from django.db import models


class CatalogWishlistProfile(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="catalogue_wishlists",
        null=True,
        blank=True,
    )
    catalogue = models.ForeignKey(
        "core_catalogs.CoreCatalogProfile",
        on_delete=models.CASCADE,
        related_name="wishlisted_by",
        null=True,
        blank=True,
    )
    user_identifier = models.CharField(max_length=255, blank=True, default="")
    product_sku = models.CharField(max_length=100, blank=True, default="")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = "catalog_wishlist"
        db_table = "catalog_wishlist_profile"

    def __str__(self):
        label = self.user.email if self.user else self.user_identifier
        cat_label = self.catalogue.name if self.catalogue else self.product_sku
        return f"Wishlist ({label}) - {cat_label}"
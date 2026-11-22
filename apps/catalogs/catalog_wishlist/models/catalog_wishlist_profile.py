from django.db import models

class CatalogWishlistProfile(models.Model):
    user_identifier = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'catalog_wishlist'
        db_table = 'catalog_wishlist_profile'

    def __str__(self):
        return f"Wishlist ({self.user_identifier}) - {self.product_sku}"
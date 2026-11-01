# apps/marketing_leads/wishlists/models/wishlists_profile.py

from django.conf import settings
from django.db import models

class WishlistProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlists')
    product_id = models.CharField(max_length=100)  # Catalog product reference
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product_id')

    def __str__(self):
        return f"Wishlist: {self.user.email} - Product {self.product_id}"
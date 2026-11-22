from django.conf import settings
from django.db import models

class Wishlist(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='marketing_wishlists'
    )
    product_id = models.IntegerField(help_text="Reference to catalog product ID")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Safe string representation using email/id to avoid startup loading issues
        user_identifier = getattr(self.user, 'email', str(self.pk))
        return f"Wishlist item for {user_identifier}"
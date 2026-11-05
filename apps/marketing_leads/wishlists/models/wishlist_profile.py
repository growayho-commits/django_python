from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketing_wishlists')
    product_id = models.IntegerField(help_text="Reference to catalog product ID")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Wishlist item for {self.user.username}"
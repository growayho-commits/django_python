# apps/marketing_leads/carts/models/cart_profile.py

from django.conf import settings
from django.db import models

class CartProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='carts', null=True, blank=True)
    session_id = models.CharField(max_length=255, blank=True, null=True)  # For guest carts
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        identifier = self.user.email if self.user else f"Guest ({self.session_id})"
        return f"Cart #{self.id} - {identifier}"


class CartItem(models.Model):
    cart = models.ForeignKey(CartProfile, on_delete=models.CASCADE, related_name='items')
    product_id = models.CharField(max_length=100)  # Catalog product reference
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.product_id} (Qty: {self.quantity})"
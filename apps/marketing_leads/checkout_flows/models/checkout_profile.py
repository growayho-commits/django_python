# apps/marketing_leads/checkout_flows/models/checkout_profile.py

from django.conf import settings
from django.db import models

class CheckoutProfile(models.Model):
    CHECKOUT_STATUS_CHOICES = [
        ('initiated', 'Initiated'),
        ('shipping_selected', 'Shipping Selected'),
        ('payment_pending', 'Payment Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='checkouts', null=True, blank=True)
    cart_id = models.CharField(max_length=100)
    status = models.CharField(max_length=30, choices=CHECKOUT_STATUS_CHOICES, default='initiated')
    shipping_address = models.TextField(blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Checkout #{self.id} - Status: {self.status}"
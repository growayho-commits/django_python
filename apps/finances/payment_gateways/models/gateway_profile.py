from django.conf import settings
from django.db import models


class PaymentGatewayConfig(models.Model):
    name = models.CharField(max_length=100, unique=True, default='Razorpay')
    provider = models.CharField(max_length=50, default='razorpay')
    is_active = models.BooleanField(default=True)
    is_test_mode = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"


class EscrowTransaction(models.Model):
    ESCROW_STATUS_CHOICES = [
        ('held', 'Held in Escrow'),
        ('released', 'Released & Split'),
        ('refunded', 'Refunded to Buyer'),
    ]

    order = models.OneToOneField(
        'orders.OrderProfile',
        on_delete=models.CASCADE,
        related_name='escrow_transaction',
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='escrow_payments',
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    gateway_name = models.CharField(max_length=100, default='Escrow / UPI')
    gateway_reference = models.CharField(max_length=150, blank=True, default='')
    escrow_status = models.CharField(max_length=20, choices=ESCROW_STATUS_CHOICES, default='held')
    held_at = models.DateTimeField(auto_now_add=True)
    released_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Escrow #{self.order.order_number} - {self.escrow_status} (INR {self.amount})"
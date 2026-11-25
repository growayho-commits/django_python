from django.conf import settings
from django.db import models


class CommissionProfile(models.Model):
    RECIPIENT_ROLE_CHOICES = [
        ('superuser', 'Superuser / Platform'),
        ('executive', 'Executive'),
        ('seller', 'Seller'),
        ('referrer', 'Referral Bonus'),
    ]

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='commissions')
    order_ref = models.ForeignKey(
        'orders.OrderProfile',
        on_delete=models.SET_NULL,
        related_name='commission_records',
        null=True,
        blank=True,
    )
    order_id = models.CharField(max_length=100)
    recipient_role = models.CharField(max_length=20, choices=RECIPIENT_ROLE_CHOICES, default='seller')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    commission_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payout_status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_role.title()} Commission for Order #{self.order_id} - {self.commission_amount}"
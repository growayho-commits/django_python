from django.conf import settings
from django.db import models


class PayoutProfile(models.Model):
    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='processing')
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Payout #{self.id} - {self.amount} ({self.status})"


class LoyaltyWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loyalty_wallet')
    loyalty_points = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    cash_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet ({self.user.email}) - Points: {self.loyalty_points} | INR {self.cash_balance}"


class WalletTransaction(models.Model):
    TX_TYPE_CHOICES = [
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    ]

    wallet = models.ForeignKey(LoyaltyWallet, on_delete=models.CASCADE, related_name='transactions')
    tx_type = models.CharField(max_length=10, choices=TX_TYPE_CHOICES, default='credit')
    points_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_delta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference_note = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tx_type.upper()} - {self.reference_note}"
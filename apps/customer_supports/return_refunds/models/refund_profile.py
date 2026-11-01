from django.conf import settings
from django.db import models

class ReturnRefundProfile(models.Model):
    REFUND_STATUS = [
        ('requested', 'Requested'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('processed', 'Processed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='returns_refunds')
    order_id = models.CharField(max_length=100)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=REFUND_STATUS, default='requested')
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Request #{self.id} - Order: {self.order_id}"
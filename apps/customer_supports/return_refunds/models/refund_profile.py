from django.db import models
from django.conf import settings

class ReturnRefundProfile(models.Model):
    REASON_CHOICES = [
        ('Defective', 'Defective / Damaged'),
        ('Wrong Item', 'Wrong Item Received'),
        ('Not Satisfied', 'Not Satisfied'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.CharField(max_length=100)
    reason = models.CharField(max_length=50, choices=REASON_CHOICES)
    description = models.TextField()
    refund_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Refund for Order: {self.order}"
from django.conf import settings
from django.db import models


class MerchantProfile(models.Model):
    MERCHANT_TYPES = (
        ('distributor', 'Distributor'),
        ('retail_merchant', 'Retail Merchant'),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='merchants_profile',
    )
    assigned_executive = models.ForeignKey(
        'executives.ExecutiveProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='assigned_merchants',
    )
    business_name = models.CharField(max_length=255, blank=True, default='')
    merchant_type = models.CharField(max_length=50, choices=MERCHANT_TYPES, default='distributor')
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.business_name and self.user_id:
            self.business_name = f"Merchant-{self.user_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.business_name} ({self.get_merchant_type_display()})"
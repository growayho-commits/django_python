from django.conf import settings
from django.db import models

class MerchantProfile(models.Model):
    MERCHANT_TYPES = (
        ('distributor', 'Distributor'),
        ('retail_merchant', 'Retail Merchant'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='merchant_profile')
    business_name = models.CharField(max_length=255)
    merchant_type = models.CharField(max_length=50, choices=MERCHANT_TYPES, default='distributor')
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.business_name} ({self.get_merchant_type_display()})"
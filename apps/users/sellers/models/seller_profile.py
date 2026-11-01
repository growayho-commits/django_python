from django.conf import settings
from django.db import models

class SellerProfile(models.Model):
    SELLER_TYPES = (
        ('manufacturer', 'Manufacturer'),
        ('dealer', 'Dealer'),
        ('wholesaler', 'Wholesaler'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_profile')
    store_name = models.CharField(max_length=255)
    seller_type = models.CharField(max_length=50, choices=SELLER_TYPES, default='wholesaler')
    gstin = models.CharField(max_length=15, unique=True, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store_name} ({self.get_seller_type_display()})"
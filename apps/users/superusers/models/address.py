from django.db import models
from django.conf import settings
from .business_profile import BusinessProfile

class UserAddress(models.Model):
    ADDRESS_TYPE_CHOICES = [
        ('BILLING', 'Billing Address'),
        ('SHIPPING', 'Shipping Address'),
        ('GST_BRANCH', 'GST Branch Address'),
        ('PICKUP', 'Pickup Address'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    business_profile = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='business_addresses'
    )
    
    address_type = models.CharField(max_length=30, choices=ADDRESS_TYPE_CHOICES)
    address_title = models.CharField(max_length=100, help_text="உதா: Home, Warehouse, Branch Office")
    contact_person_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=15)
    
    address_line1 = models.TextField()
    address_line2 = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    gstin_number = models.CharField(max_length=50, blank=True, null=True)
    is_default = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.address_title} ({self.get_address_type_display()}) - {self.city}"
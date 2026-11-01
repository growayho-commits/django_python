# apps/users/guests/models/business_profile.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class BusinessProfile(models.Model):
    """
    Merchants, Sellers மற்றும் B2B2C/C2C பயனர்களுக்கான வணிகச் சுயவிவரம்.
    விற்பனையாளராக மாறும் போது மட்டும் இந்த விவரங்கள் நிரப்பப்படும் (Optional).
    """
    class BusinessType(models.TextChoices):
        INDIVIDUAL = 'INDIVIDUAL', _('Individual / MSME')
        PROPRIETORSHIP = 'PROPRIETORSHIP', _('Proprietorship')
        PARTNERSHIP = 'PARTNERSHIP', _('Partnership Firm')
        PRIVATE_LIMITED = 'PVT_LTD', _('Private Limited')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_profile')
    
    # வணிக விவரங்கள்
    company_name = models.CharField(max_length=255, null=True, blank=True)
    business_type = models.CharField(max_length=20, choices=BusinessType.choices, default=BusinessType.INDIVIDUAL, null=True, blank=True)
    display_handle = models.CharField(max_length=100, unique=True, null=True, blank=True, help_text=_('Shop Handle Name'))
    
    # வரி மற்றும் சான்றிதழ்கள் (Optional)
    gstin_or_tax_id = models.CharField(max_length=50, null=True, blank=True)
    msme_registration_number = models.CharField(max_length=100, null=True, blank=True)
    is_verified_business = models.BooleanField(default=False)

    # வர்த்தக & B2B/C2C கட்டுப்பாடுகள்
    commission_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    rating_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"BusinessProfile for {self.user.email}"
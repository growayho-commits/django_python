from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Address(models.Model):
    class AddressType(models.TextChoices):
        HOME = 'HOME', _('வீடு')
        WORK = 'WORK', _('அலுவலகம்')
        WAREHOUSE = 'WAREHOUSE', _('கிடங்கு / தொழிற்சாலை')

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='addresses'
    )
    full_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=150, blank=True)
    
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')

    # மேப் மற்றும் லாஜிஸ்டிக்ஸிற்கான ஜிபிஎஸ் ஒருங்கிணைப்பு
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    address_type = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.HOME)
    is_default_shipping = models.BooleanField(default=False)
    is_default_billing = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('முகவரி')
        verbose_name_plural = _('முகவரிகள் (Addresses)')
        ordering = ['-is_default_shipping', '-created_at']

    def save(self, *args, **kwargs):
        if self.is_default_shipping:
            Address.objects.filter(user=self.user, is_default_shipping=True).update(is_default_shipping=False)
        if self.is_default_billing:
            Address.objects.filter(user=self.user, is_default_billing=True).update(is_default_billing=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.full_name} - {self.postal_code} ({self.address_type})"
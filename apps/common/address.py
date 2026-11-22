from django.db import models
from apps.common.models import BaseModel  # BaseModel-ஐயும் இங்கேயே அல்லது base.py-ல் வைத்துக் கொள்ளலாம்

class Address(BaseModel):
    """
    ப்ராஜெக்ட் முழுவதும் பொதுவாகப் பயன்படுத்தப்படும் அட்ரஸ் மாடல் (Address Model)
    """
    address_line_1 = models.CharField(max_length=255, verbose_name="Address Line 1")
    address_line_2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Address Line 2")
    landmark = models.CharField(max_length=150, blank=True, null=True, verbose_name="Landmark")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    country = models.CharField(max_length=100, default='India', verbose_name="Country")
    pincode = models.CharField(max_length=20, verbose_name="Pincode")
    
    # விருப்பப்பட்டால் ஜிபிஎஸ் லொகேஷன் சேர்த்துக்கொள்ளலாம்
    latitude = models.DecimalField(max_digits=9, decimal_latitude=6, blank=True, null=True) if hasattr(models, 'DecimalField') else None # Optional GPS
    longitude = models.DecimalField(max_digits=9, decimal_longitude=6, blank=True, null=True) if hasattr(models, 'DecimalField') else None

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.city}, {self.state} - {self.pincode}"
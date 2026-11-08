from django.db import models
from django.conf import settings

class BusinessProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business_profile')
    company_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100, blank=True, null=True, help_text="Sole Proprietorship, Pvt Ltd, etc.")
    
    gst_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    pan_number = models.CharField(max_length=50, blank=True, null=True)
    
    business_address = models.TextField()
    business_city = models.CharField(max_length=100)
    business_state = models.CharField(max_length=100)
    business_pincode = models.CharField(max_length=10)
    
    business_email = models.EmailField(blank=True, null=True)
    business_phone = models.CharField(max_length=15, blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Business: {self.company_name} (Owner: {self.user.email})"
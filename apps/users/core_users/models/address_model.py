from django.conf import settings
from django.db import models

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    address_line = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    
    gstin = models.CharField(max_length=15, blank=True, null=True)
    is_gst_within_state = models.BooleanField(default=True)
    authorization_letter = models.FileField(upload_to='auth_letters/', blank=True, null=True)
    
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city}, {self.state} - {self.pincode}"
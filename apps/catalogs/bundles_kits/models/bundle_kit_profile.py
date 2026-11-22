from django.db import models

class BundleKitProfile(models.Model):
    bundle_name = models.CharField(max_length=255, unique=True)
    bundle_sku = models.CharField(max_length=100, unique=True)
    bundle_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bundle_name
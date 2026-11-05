from django.db import models
from django.conf import settings

class CoreCatalog(models.Model):
    VISIBILITY_CHOICES = [
        ('bulk_only', 'Bulk Only (Sellers Only)'),
        ('retail_only', 'Retail Only (Members Only)'),
        ('both', 'Both Bulk & Retail (Sellers & Members)'),
    ]

    vendor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=255)
    description = models.TextField()
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='both')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.sku}) - {self.get_visibility_display()}"
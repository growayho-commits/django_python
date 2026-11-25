from django.conf import settings
from django.db import models


class CustomerLeadProfile(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='rfq_leads',
        null=True,
        blank=True,
    )
    catalogue = models.ForeignKey(
        'core_catalogs.CoreCatalogProfile',
        on_delete=models.SET_NULL,
        related_name='rfq_leads',
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    requested_quantity = models.PositiveIntegerField(default=1)
    target_unit_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    notes = models.TextField(blank=True, default='')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, null=True)  # e.g., B2B RFQ, Ads, Referral
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead: {self.full_name} ({self.status})"
# apps/marketing_leads/customer_leads/models/lead_profile.py

from django.db import models

class CustomerLeadProfile(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('qualified', 'Qualified'),
        ('converted', 'Converted'),
        ('lost', 'Lost'),
    ]

    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='new')
    source = models.CharField(max_length=100, blank=True, null=True)  # e.g., Ads, Referral, Organic
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Lead: {self.full_name} ({self.status})"
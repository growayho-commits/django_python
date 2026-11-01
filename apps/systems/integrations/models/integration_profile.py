# apps/systems/integrations/models/integration_profile.py

from django.db import models

class IntegrationProfile(models.Model):
    service_name = models.CharField(max_length=150, unique=True)  # e.g., 'Stripe', 'Firebase', 'SendGrid'
    api_key = models.CharField(max_length=255, blank=True, null=True)
    api_secret = models.CharField(max_length=255, blank=True, null=True)
    webhook_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Integration: {self.service_name} ({'Active' if self.is_active else 'Inactive'})"
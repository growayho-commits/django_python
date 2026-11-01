from django.db import models

class LogisticsPartnerProfile(models.Model):
    partner_name = models.CharField(max_length=100, unique=True)
    tracking_url_template = models.URLField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.partner_name
# apps/marketing_leads/ads_campaigns/models/campaign_profile.py

from django.db import models

class AdsCampaignProfile(models.Model):
    CAMPAIGN_TYPES = [
        ('social_media', 'Social Media'),
        ('search_engine', 'Search Engine'),
        ('banner', 'Banner Ad'),
        ('email', 'Email Campaign'),
    ]

    campaign_name = models.CharField(max_length=255, unique=True)
    campaign_type = models.CharField(max_length=50, choices=CAMPAIGN_TYPES, default='social_media')
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    clicks = models.PositiveIntegerField(default=0)
    conversions = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.campaign_name} ({self.get_campaign_type_display()})"
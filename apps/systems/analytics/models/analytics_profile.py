# apps/systems/analytics/models/analytics_profile.py

from django.db import models

class AnalyticsProfile(models.Model):
    metric_name = models.CharField(max_length=150, unique=True)
    metric_value = models.DecimalField(max_digits=15, decimal_places=4, default=0.0000)
    category = models.CharField(max_length=100, blank=True, null=True)  # e.g., Sales, Traffic, Users
    recorded_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.metric_name}: {self.metric_value}"
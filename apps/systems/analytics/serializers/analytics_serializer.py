# apps/systems/analytics/serializers/analytics_serializer.py

from rest_framework import serializers
from ..models.analytics_profile import AnalyticsProfile

class AnalyticsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalyticsProfile
        fields = ['id', 'metric_name', 'metric_value', 'category', 'recorded_date', 'updated_at']
        read_only_fields = ['id', 'recorded_date', 'updated_at']
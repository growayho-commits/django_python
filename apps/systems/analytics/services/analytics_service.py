# apps/systems/analytics/services/analytics_service.py

from ..models.analytics_profile import AnalyticsProfile

class AnalyticsService:
    @staticmethod
    def update_or_create_metric(metric_name, value, category=None):
        profile, created = AnalyticsProfile.objects.update_or_create(
            metric_name=metric_name,
            defaults={'metric_value': value, 'category': category}
        )
        return profile

    @staticmethod
    def get_metric(metric_name):
        try:
            return AnalyticsProfile.objects.get(metric_name=metric_name)
        except AnalyticsProfile.DoesNotExist:
            raise ValueError("Metric not found.")
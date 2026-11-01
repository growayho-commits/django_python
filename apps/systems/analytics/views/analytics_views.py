# apps/systems/analytics/views/analytics_views.py

from rest_framework import viewsets, permissions
from ..models.analytics_profile import AnalyticsProfile
from ..serializers.analytics_serializer import AnalyticsProfileSerializer

class AnalyticsProfileViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsProfile.objects.all()
    serializer_class = AnalyticsProfileSerializer
    permission_classes = [permissions.IsAdminUser]
# apps/systems/integrations/views/integration_views.py

from rest_framework import viewsets, permissions
from ..models.integration_profile import IntegrationProfile
from ..serializers.integration_serializer import IntegrationProfileSerializer

class IntegrationProfileViewSet(viewsets.ModelViewSet):
    queryset = IntegrationProfile.objects.all()
    serializer_class = IntegrationProfileSerializer
    permission_classes = [permissions.IsAdminUser]
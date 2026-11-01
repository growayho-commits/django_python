# apps/marketing_leads/customer_leads/views/lead_views.py

from rest_framework import viewsets, permissions
from ..models.lead_profile import CustomerLeadProfile
from ..serializers.lead_serializer import CustomerLeadSerializer

class CustomerLeadViewSet(viewsets.ModelViewSet):
    queryset = CustomerLeadProfile.objects.all()
    serializer_class = CustomerLeadSerializer
    permission_classes = [permissions.IsAuthenticated]
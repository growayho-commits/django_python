# apps/marketing_leads/checkout_flows/views/checkout_views.py

from rest_framework import viewsets, permissions
from ..models.checkout_profile import CheckoutProfile
from ..serializers.checkout_serializer import CheckoutProfileSerializer

class CheckoutViewSet(viewsets.ModelViewSet):
    queryset = CheckoutProfile.objects.all()
    serializer_class = CheckoutProfileSerializer
    permission_classes = [permissions.AllowAny]
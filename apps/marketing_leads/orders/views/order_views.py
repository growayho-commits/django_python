# apps/marketing_leads/orders/views/order_views.py

from rest_framework import viewsets, permissions
from ..models.order_profile import OrderProfile
from ..serializers.order_serializer import OrderProfileSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderProfile.objects.all()
        return OrderProfile.objects.filter(user=user)
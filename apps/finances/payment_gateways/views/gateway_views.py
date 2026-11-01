from rest_framework import viewsets, permissions
from ..models.gateway_profile import PaymentGatewayConfig
from ..serializers.gateway_serializer import PaymentGatewayConfigSerializer

class PaymentGatewayViewSet(viewsets.ModelViewSet):
    queryset = PaymentGatewayConfig.objects.all()
    serializer_class = PaymentGatewayConfigSerializer
    permission_classes = [permissions.IsAdminUser]
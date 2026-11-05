from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.marketing_leads.orders.models import OrderProfile, OrderItem
from apps.marketing_leads.orders.serializers.order_serializer import OrderProfileSerializer, OrderItemSerializer

class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderProfileSerializer

    def get_queryset(self):
        user = self.request.user
        # சூப்பர் யூசர்கள் அல்லது எக்சிகியூட்டிவ்கள் அனைத்து ஆர்டர்களையும் பார்க்கலாம், மற்றவர்கள் தங்களது ஆர்டர்களை மட்டும் பார்க்கலாம்
        if user.is_staff or user.is_superuser:
            return OrderProfile.objects.all()
        return OrderProfile.objects.filter(user=user)

    def perform_create(self, serializer):
        # ஆர்டரை உருவாக்கும் போது பயனரை இணைத்தல்
        serializer.save(user=self.request.user)


class OrderItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__user=user)
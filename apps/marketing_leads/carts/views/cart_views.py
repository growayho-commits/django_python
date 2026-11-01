# apps/marketing_leads/carts/views/cart_views.py

from rest_framework import viewsets, permissions
from ..models.cart_profile import CartProfile
from ..serializers.cart_serializer import CartProfileSerializer
from ..services.cart_service import CartService

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return CartProfile.objects.filter(user=user)
        session_id = self.request.session.session_key
        if session_id:
            return CartProfile.objects.filter(session_id=session_id)
        return CartProfile.objects.none()
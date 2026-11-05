from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from apps.marketing_leads.carts.models import CartProfile, CartItem
from apps.marketing_leads.carts.serializers.cart_serializer import CartProfileSerializer, CartItemSerializer

class CartViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartProfileSerializer

    def get_queryset(self):
        # ஒவ்வொரு பயனருக்கும் பிரத்யேகமான கார்ட்டை வழங்க அல்லது உருவாக்க
        cart, created = CartProfile.objects.get_or_create(user=self.request.user)
        return CartProfile.objects.filter(pk=cart.pk)

    def list(self, request, *args, **kwargs):
        cart, _ = CartProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        cart, _ = CartProfile.objects.get_or_create(user=self.request.user)
        return CartItem.objects.filter(cart=cart)

    def perform_create(self, serializer):
        cart, _ = CartProfile.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)
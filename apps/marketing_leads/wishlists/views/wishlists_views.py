# apps/marketing_leads/wishlists/views/wishlists_views.py

from rest_framework import viewsets, permissions
from ..models.wishlists_profile import WishlistProfile
from ..serializers.wishlists_serializer import WishlistSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WishlistProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
from rest_framework import viewsets, permissions
from apps.marketing_leads.wishlists.models import Wishlist
from apps.marketing_leads.wishlists.serializers import WishlistSerializer

class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
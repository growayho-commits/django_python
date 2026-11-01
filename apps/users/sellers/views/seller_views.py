from rest_framework import generics, permissions
from apps.users.sellers.models import SellerProfile
from apps.users.sellers.serializers import SellerProfileSerializer

class SellerProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = SellerProfile.objects.get_or_create(user=self.request.user)
        return profile
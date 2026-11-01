from rest_framework import generics, permissions
from apps.users.merchant.models import MerchantProfile
from apps.users.merchant.serializers import MerchantProfileSerializer

class MerchantProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = MerchantProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = MerchantProfile.objects.get_or_create(user=self.request.user)
        return profile
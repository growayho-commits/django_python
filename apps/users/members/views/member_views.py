from rest_framework import generics, permissions
from apps.users.members.models import MemberProfile
from apps.users.members.serializers import MemberProfileSerializer

class MemberProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = MemberProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = MemberProfile.objects.get_or_create(user=self.request.user)
        return profile
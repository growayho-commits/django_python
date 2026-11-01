from rest_framework import generics, permissions
from apps.users.executives.models import ExecutiveProfile
from apps.users.executives.serializers import ExecutiveProfileSerializer

class ExecutiveProfileCreateOrUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = ExecutiveProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, created = ExecutiveProfile.objects.get_or_create(user=self.request.user)
        return profile
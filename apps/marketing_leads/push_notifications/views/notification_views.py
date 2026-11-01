# apps/marketing_leads/push_notifications/views/notification_views.py

from rest_framework import viewsets, permissions
from ..models.notification_profile import PushNotificationProfile
from ..serializers.notification_serializer import PushNotificationSerializer

class PushNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = PushNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return PushNotificationProfile.objects.all()
        return PushNotificationProfile.objects.filter(user=user)
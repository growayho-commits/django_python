# apps/marketing_leads/push_notifications/serializers/notification_serializer.py

from rest_framework import serializers
from ..models.notification_profile import PushNotificationProfile

class PushNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PushNotificationProfile
        fields = ['id', 'user', 'title', 'message', 'is_read', 'sent_at']
        read_only_fields = ['id', 'sent_at']
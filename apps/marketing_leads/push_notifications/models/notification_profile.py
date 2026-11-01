# apps/marketing_leads/push_notifications/models/notification_profile.py

from django.conf import settings
from django.db import models

class PushNotificationProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        recipient = self.user.email if self.user else "Broadcast / All Users"
        return f"Notification to {recipient} - {self.title}"
# apps/marketing_leads/push_notifications/services/notification_service.py

from ..models.notification_profile import PushNotificationProfile

class PushNotificationService:
    @staticmethod
    def send_notification(user, title, message):
        notification = PushNotificationProfile.objects.create(
            user=user,
            title=title,
            message=message
        )
        return notification

    @staticmethod
    def mark_as_read(notification_id):
        try:
            notification = PushNotificationProfile.objects.get(id=notification_id)
            notification.is_read = True
            notification.save()
            return notification
        except PushNotificationProfile.DoesNotExist:
            raise ValueError("Notification not found.")
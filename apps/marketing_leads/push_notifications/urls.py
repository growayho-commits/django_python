from django.urls import path
from .views.notification_views import PushNotificationViewSet

app_name = 'push_notifications'

urlpatterns = [
    path('push-notification/', PushNotificationViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='push_notification'),
]

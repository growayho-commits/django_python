from django.urls import path
from .views.notification_views import PushNotificationViewSet
from .views.notification_portal_views import notifications_inbox_view

app_name = 'push_notifications'

urlpatterns = [
    path('push-notification/', PushNotificationViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='push_notification'),
    path('portal/', notifications_inbox_view, name='notifications_inbox'),
]
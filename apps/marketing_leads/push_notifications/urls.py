# apps/marketing_leads/push_notifications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.notification_views import PushNotificationViewSet

router = DefaultRouter()
router.register(r'notifications', PushNotificationViewSet, basename='push-notifications')

urlpatterns = [
    path('', include(router.urls)),
]
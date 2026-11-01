from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.gateway_views import PaymentGatewayViewSet

router = DefaultRouter()
router.register(r'gateways', PaymentGatewayViewSet, basename='payment-gateways')

urlpatterns = [
    path('', include(router.urls)),
]
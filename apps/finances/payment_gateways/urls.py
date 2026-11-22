from django.urls import path
from .views.gateway_views import PaymentGatewayViewSet

app_name = 'payment_gateways'

urlpatterns = [
    path('payment-gateway/', PaymentGatewayViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='payment_gateway'),
]

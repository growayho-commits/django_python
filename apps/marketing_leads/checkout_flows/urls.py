from django.urls import path
from .views.checkout_views import CheckoutViewSet

app_name = 'checkout_flows'

urlpatterns = [
    path('checkout/', CheckoutViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='checkout'),
]

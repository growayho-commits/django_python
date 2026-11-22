from django.urls import path
from .views.order_views import OrderViewSet, OrderItemViewSet

app_name = 'orders'

urlpatterns = [
    path('order/', OrderViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='order'),
    path('order-item/', OrderItemViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='order_item'),
]

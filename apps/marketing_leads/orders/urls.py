from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.order_portal_views import my_orders_view, order_detail_view
from .views.order_views import OrderItemViewSet, OrderViewSet

app_name = 'orders'

router = DefaultRouter()
router.register(r'order', OrderViewSet, basename='order')
router.register(r'order-item', OrderItemViewSet, basename='order-item')

urlpatterns = [
    path('my-orders/', my_orders_view, name='my_orders'),
    path('my-orders/<int:pk>/', order_detail_view, name='order_detail'),
    path('', include(router.urls)),
]
from django.urls import path
from .views.cart_views import CartViewSet, CartItemViewSet

app_name = 'carts'

urlpatterns = [
    path('cart/', CartViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='cart'),
    path('cart-item/', CartItemViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='cart_item'),
]

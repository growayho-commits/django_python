from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.cart_portal_views import my_cart_view
from .views.cart_views import CartItemViewSet, CartViewSet

app_name = 'carts'

router = DefaultRouter()
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'cart-item', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('my-cart/', my_cart_view, name='my_cart'),
    path('', include(router.urls)),
]
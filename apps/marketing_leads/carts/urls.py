# apps/marketing_leads/carts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.cart_views import CartViewSet

router = DefaultRouter()
router.register(r'carts', CartViewSet, basename='carts')

urlpatterns = [
    path('', include(router.urls)),
]
# apps/marketing_leads/checkout_flows/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.checkout_views import CheckoutViewSet

router = DefaultRouter()
router.register(r'checkouts', CheckoutViewSet, basename='checkouts')

urlpatterns = [
    path('', include(router.urls)),
]
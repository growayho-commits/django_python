from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views.checkout_portal_views import checkout_portal_view
from .views.checkout_views import CheckoutViewSet

app_name = 'checkout_flows'

router = DefaultRouter()
router.register(r'checkout', CheckoutViewSet, basename='checkout')

urlpatterns = [
    path('portal/', checkout_portal_view, name='checkout_portal'),
    path('', include(router.urls)),
]
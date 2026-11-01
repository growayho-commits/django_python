# apps/marketing_leads/coupons_discounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.coupon_views import CouponDiscountViewSet

router = DefaultRouter()
router.register(r'coupons', CouponDiscountViewSet, basename='coupons')

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path
from .views.coupon_views import CouponDiscountViewSet

app_name = 'coupons_discounts'

urlpatterns = [
    path('coupon-discount/', CouponDiscountViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='coupon_discount'),
]

from django.urls import path
from .views.coupon_views import CouponDiscountViewSet
from .views.coupon_portal_views import manage_coupons_view

app_name = 'coupons_discounts'

urlpatterns = [
    path('coupon-discount/', CouponDiscountViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update', 'delete': 'destroy'}), name='coupon_discount'),
    path('portal/', manage_coupons_view, name='manage_coupons'),
]
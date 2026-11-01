# apps/marketing_leads/coupons_discounts/views/coupon_views.py

from rest_framework import viewsets, permissions
from ..models.coupon_profile import CouponDiscountProfile
from ..serializers.coupon_serializer import CouponDiscountSerializer

class CouponDiscountViewSet(viewsets.ModelViewSet):
    queryset = CouponDiscountProfile.objects.all()
    serializer_class = CouponDiscountSerializer
    permission_classes = [permissions.IsAdminUser]
# apps/marketing_leads/coupons_discounts/serializers/coupon_serializer.py

from rest_framework import serializers
from ..models.coupon_profile import CouponDiscountProfile

class CouponDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = CouponDiscountProfile
        fields = ['id', 'code', 'discount_type', 'discount_value', 'min_purchase_amount', 'is_active', 'valid_from', 'valid_until', 'created_at']
        read_only_fields = ['id', 'created_at']
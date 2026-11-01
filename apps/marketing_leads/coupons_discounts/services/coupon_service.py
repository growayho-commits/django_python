# apps/marketing_leads/coupons_discounts/services/coupon_service.py

from django.utils import timezone
from ..models.coupon_profile import CouponDiscountProfile

class CouponService:
    @staticmethod
    def validate_and_apply_coupon(code, cart_total):
        try:
            coupon = CouponDiscountProfile.objects.get(code=code, is_active=True)
            now = timezone.now()
            
            if not (coupon.valid_from <= now <= coupon.valid_until):
                raise ValueError("Coupon is expired or not yet active.")
            
            if cart_total < coupon.min_purchase_amount:
                raise ValueError(f"Minimum purchase amount of {coupon.min_purchase_amount} required.")
            
            if coupon.discount_type == 'percentage':
                discount_amount = (cart_total * coupon.discount_value) / 100
            else:
                discount_amount = coupon.discount_value
                
            return max(cart_total - discount_amount, 0), discount_amount
            
        except CouponDiscountProfile.DoesNotExist:
            raise ValueError("Invalid coupon code.")
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.marketing_leads.coupons_discounts.models.coupon_profile import CouponDiscountProfile
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def _can_manage_coupons(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "marketing_leads" in activities
    return False


@login_required
def manage_coupons_view(request):
    """Create, list, and toggle active coupons."""
    can_manage = _can_manage_coupons(request.user)

    if request.method == "POST" and can_manage:
        action = request.POST.get("action")
        if action == "create_coupon":
            code = request.POST.get("code", "").strip().upper()
            discount_type = request.POST.get("discount_type", "percentage")
            discount_value = request.POST.get("discount_value") or 0
            min_purchase = request.POST.get("min_purchase_amount") or 0
            days_valid = max(1, int(request.POST.get("days_valid") or 30))
            now = timezone.now()

            if code:
                try:
                    CouponDiscountProfile.objects.create(
                        code=code,
                        discount_type=discount_type,
                        discount_value=discount_value,
                        min_purchase_amount=min_purchase,
                        is_active=True,
                        valid_from=now,
                        valid_until=now + timedelta(days=days_valid),
                    )
                    messages.success(request, f"Coupon '{code}' created for {days_valid} days.")
                except IntegrityError:
                    messages.error(request, f"Coupon code '{code}' already exists.")

        elif action == "toggle_coupon":
            coupon = get_object_or_404(CouponDiscountProfile, pk=request.POST.get("coupon_id"))
            coupon.is_active = not coupon.is_active
            coupon.save(update_fields=["is_active"])
            messages.info(request, f"Coupon '{coupon.code}' status updated.")

        return redirect("coupons_discounts:manage_coupons")

    coupons = CouponDiscountProfile.objects.all().order_by("-created_at")
    return render(request, "coupons_discounts/manage_coupons.html", {
        "coupons": coupons,
        "can_manage": can_manage,
    })
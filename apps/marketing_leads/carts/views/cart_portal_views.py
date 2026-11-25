from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils import timezone

from apps.marketing_leads.carts.services.cart_service import CartCheckoutService
from apps.marketing_leads.coupons_discounts.models.coupon_profile import CouponDiscountProfile


@login_required
def my_cart_view(request):
    """Display buyer cart, update quantities, remove items, and apply coupon codes."""
    if request.method == "POST":
        action = request.POST.get("action")
        cart = request.session.get("hm_cart", {})

        if action == "update_qty":
            cart_key = request.POST.get("cart_key", "")
            if cart_key in cart:
                try:
                    new_qty = max(1, int(request.POST.get("quantity") or 1))
                except ValueError:
                    new_qty = 1
                cart[cart_key]["quantity"] = new_qty
                request.session["hm_cart"] = cart
                request.session.modified = True
                messages.success(request, "Cart quantity updated.")

        elif action == "remove_item":
            cart_key = request.POST.get("cart_key", "")
            if cart_key in cart:
                del cart[cart_key]
                request.session["hm_cart"] = cart
                request.session.modified = True
                messages.info(request, "Item removed from cart.")

        elif action == "apply_coupon":
            code = request.POST.get("coupon_code", "").strip()
            now = timezone.now()
            coupon = CouponDiscountProfile.objects.filter(
                code__iexact=code,
                is_active=True,
                valid_from__lte=now,
                valid_until__gte=now,
            ).first()
            if not coupon:
                messages.error(request, "Invalid or expired coupon code.")
            else:
                request.session["hm_coupon"] = coupon.code
                request.session.modified = True
                messages.success(request, f"Coupon '{coupon.code}' applied.")

        elif action == "remove_coupon":
            request.session.pop("hm_coupon", None)
            request.session.modified = True
            messages.info(request, "Coupon removed.")

        return redirect("carts:my_cart")

    summary = CartCheckoutService.build_cart_summary(request)
    return render(request, "carts/my_cart.html", {"summary": summary})
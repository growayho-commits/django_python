from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from apps.marketing_leads.carts.services.cart_service import CartCheckoutService
from apps.users.superusers.models.address import UserAddress


@login_required
def checkout_portal_view(request):
    """Checkout page with address confirmation, payment method selection, and order placement."""
    summary = CartCheckoutService.build_cart_summary(request)
    if not summary["items"]:
        messages.warning(request, "Your cart is empty. Add catalogues before checking out.")
        return redirect("catalogs:core_catalogs:catalogue_marketplace")

    default_addr = UserAddress.objects.filter(user=request.user).order_by("-is_default", "-id").first()
    prefill_address = ""
    if default_addr:
        parts = [
            default_addr.address_line_1,
            default_addr.address_line_2,
            default_addr.city,
            default_addr.district,
            default_addr.state,
            default_addr.pincode,
        ]
        prefill_address = ", ".join(p for p in parts if p)

    if request.method == "POST":
        shipping_address = request.POST.get("shipping_address", "").strip()
        billing_address = request.POST.get("billing_address", "").strip() or shipping_address
        payment_method = request.POST.get("payment_method", "cod").strip()

        if not shipping_address:
            messages.error(request, "Please enter a shipping address.")
        else:
            try:
                order = CartCheckoutService.place_order_from_cart(
                    request=request,
                    shipping_address=shipping_address,
                    billing_address=billing_address,
                    payment_method=payment_method,
                )
                messages.success(request, f"Order {order.order_number} placed successfully!")
                return redirect("orders:order_detail", pk=order.pk)
            except ValueError as exc:
                messages.error(request, str(exc))

    return render(request, "checkout_flows/checkout_portal.html", {
        "summary": summary,
        "prefill_address": prefill_address,
    })
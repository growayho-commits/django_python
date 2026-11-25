from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.marketing_leads.orders.models.order_profile import OrderProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


@login_required
def my_orders_view(request):
    """Buyer order history + incoming orders for Seller / Merchant / Superuser."""
    current_role = (get_user_current_role(request.user) or "member").lower()
    if request.user.is_superuser:
        current_role = "superuser"

    my_orders = OrderProfile.objects.filter(user=request.user).prefetch_related("items__catalogue").order_by("-created_at")

    incoming_orders = []
    if current_role == "superuser":
        incoming_orders = OrderProfile.objects.prefetch_related("items__catalogue").order_by("-created_at")
    elif current_role in {"seller", "merchant", "executive"}:
        incoming_orders = (
            OrderProfile.objects.filter(items__catalogue__owner=request.user)
            .distinct()
            .prefetch_related("items__catalogue")
            .order_by("-created_at")
        )

    return render(request, "orders/my_orders.html", {
        "current_role": current_role,
        "my_orders": my_orders,
        "incoming_orders": incoming_orders,
    })


@login_required
def order_detail_view(request, pk):
    """Order detail receipt & status management."""
    order = get_object_or_404(OrderProfile.objects.prefetch_related("items__catalogue"), pk=pk)
    is_buyer = order.user_id == request.user.id
    is_seller_owner = order.items.filter(catalogue__owner=request.user).exists()
    can_update_status = request.user.is_superuser or is_seller_owner

    if not (is_buyer or can_update_status):
        messages.error(request, "Permission denied.")
        return redirect("orders:my_orders")

    if request.method == "POST" and can_update_status:
        new_status = request.POST.get("status", "").strip()
        valid_statuses = {choice[0] for choice in OrderProfile.ORDER_STATUS_CHOICES}
        if new_status in valid_statuses:
            order.status = new_status
            order.save(update_fields=["status"])
            messages.success(request, f"Order {order.order_number} status updated to {order.get_status_display()}.")
        return redirect("orders:order_detail", pk=order.pk)

    return render(request, "orders/order_detail.html", {
        "order": order,
        "can_update_status": can_update_status,
        "status_choices": OrderProfile.ORDER_STATUS_CHOICES,
    })
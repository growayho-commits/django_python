import uuid

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.logistics.logistics_partners.models.partner_profile import LogisticsPartnerProfile
from apps.logistics.returns.models.return_profile import LogisticsReturnProfile
from apps.logistics.shipments.models.shipment_profile import ShipmentProfile
from apps.logistics.warehouse_transfers.models.transfer_profile import WarehouseTransferProfile
from apps.marketing_leads.orders.models.order_profile import OrderProfile
from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def _can_manage_logistics(user) -> bool:
    if user.is_superuser:
        return True
    role = (get_user_current_role(user) or "").lower()
    if role in {"seller", "merchant"}:
        return True
    if role == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "logistics" in activities
    return False


@login_required
def logistics_dashboard_view(request):
    """Shipments, Live Tracking, and Logistics Partner management."""
    can_manage = _can_manage_logistics(request.user)
    is_admin = request.user.is_superuser or (get_user_current_role(request.user) == "executive")

    if request.method == "POST" and can_manage:
        action = request.POST.get("action")

        if action == "create_shipment":
            order_id = request.POST.get("order_id", "").strip()
            partner_id = request.POST.get("partner_id") or None
            tracking_number = request.POST.get("tracking_number", "").strip() or f"TRK-{uuid.uuid4().hex[:8].upper()}"
            partner = LogisticsPartnerProfile.objects.filter(pk=partner_id).first() if partner_id else None

            if order_id:
                try:
                    shipment = ShipmentProfile.objects.create(
                        order_id=order_id,
                        partner=partner,
                        tracking_number=tracking_number,
                        status="dispatched",
                        shipped_at=timezone.now(),
                    )
                    order = OrderProfile.objects.filter(order_number=order_id).first()
                    if order:
                        order.status = "shipped"
                        order.save(update_fields=["status"])
                        PushNotificationProfile.objects.create(
                            user=order.user,
                            title=f"Order {order.order_number} Shipped",
                            message=f"Tracking #{shipment.tracking_number} via {partner.partner_name if partner else 'Carrier'}.",
                        )
                    messages.success(request, f"Shipment '{tracking_number}' created for Order {order_id}.")
                except IntegrityError:
                    messages.error(request, "Shipment already exists for this Order or Tracking Number.")

        elif action == "update_shipment_status":
            shipment = get_object_or_404(ShipmentProfile, pk=request.POST.get("shipment_id"))
            new_status = request.POST.get("status", "")
            if new_status in {c[0] for c in ShipmentProfile.STATUS_CHOICES}:
                shipment.status = new_status
                if new_status == "dispatched" and not shipment.shipped_at:
                    shipment.shipped_at = timezone.now()
                elif new_status == "delivered":
                    shipment.delivered_at = timezone.now()
                    OrderProfile.objects.filter(order_number=shipment.order_id).update(status="delivered")
                shipment.save()
                messages.success(request, f"Shipment {shipment.tracking_number} updated to {shipment.get_status_display()}.")

        elif action == "add_partner" and is_admin:
            partner_name = request.POST.get("partner_name", "").strip()
            tracking_url = request.POST.get("tracking_url_template", "").strip()
            if partner_name:
                try:
                    LogisticsPartnerProfile.objects.create(
                        partner_name=partner_name,
                        tracking_url_template=tracking_url or None,
                        is_active=True,
                    )
                    messages.success(request, f"Logistics partner '{partner_name}' added.")
                except IntegrityError:
                    messages.error(request, f"Partner '{partner_name}' already exists.")

        return redirect("logistics:logistics_dashboard")

    track_query = request.GET.get("track", "").strip()
    tracked_shipment = None
    if track_query:
        tracked_shipment = ShipmentProfile.objects.select_related("partner").filter(
            Q(tracking_number__iexact=track_query) | Q(order_id__iexact=track_query)
        ).first()

    if is_admin:
        shipments = ShipmentProfile.objects.select_related("partner").order_by("-created_at")[:50]
        orders = OrderProfile.objects.order_by("-created_at")[:50]
    elif can_manage:
        own_order_nums = list(
            OrderProfile.objects.filter(
                Q(user=request.user) | Q(items__catalogue__owner=request.user)
            ).values_list("order_number", flat=True).distinct()
        )
        shipments = ShipmentProfile.objects.select_related("partner").filter(order_id__in=own_order_nums).order_by("-created_at")
        orders = OrderProfile.objects.filter(order_number__in=own_order_nums).order_by("-created_at")
    else:
        own_order_nums = list(OrderProfile.objects.filter(user=request.user).values_list("order_number", flat=True))
        shipments = ShipmentProfile.objects.select_related("partner").filter(order_id__in=own_order_nums).order_by("-created_at")
        orders = []

    partners = LogisticsPartnerProfile.objects.filter(is_active=True).order_by("partner_name")

    return render(request, "logistics/logistics_dashboard.html", {
        "can_manage": can_manage,
        "is_admin": is_admin,
        "shipments": shipments,
        "orders": orders,
        "partners": partners,
        "status_choices": ShipmentProfile.STATUS_CHOICES,
        "track_query": track_query,
        "tracked_shipment": tracked_shipment,
    })


@login_required
def warehouse_transfers_portal_view(request):
    """Manage inter-warehouse stock transfers."""
    can_manage = _can_manage_logistics(request.user)
    if request.method == "POST" and can_manage:
        action = request.POST.get("action")
        if action == "create_transfer":
            ref = request.POST.get("transfer_reference", "").strip() or f"TRF-{uuid.uuid4().hex[:8].upper()}"
            src = request.POST.get("source_warehouse", "").strip()
            dst = request.POST.get("destination_warehouse", "").strip()
            if src and dst:
                try:
                    WarehouseTransferProfile.objects.create(
                        transfer_reference=ref,
                        source_warehouse=src,
                        destination_warehouse=dst,
                        status="initiated",
                    )
                    messages.success(request, f"Transfer '{ref}' initiated.")
                except IntegrityError:
                    messages.error(request, "Transfer reference already exists.")

        elif action == "update_transfer":
            trf = get_object_or_404(WarehouseTransferProfile, pk=request.POST.get("transfer_id"))
            new_status = request.POST.get("status", "")
            if new_status in {c[0] for c in WarehouseTransferProfile.TRANSFER_STATUS}:
                trf.status = new_status
                trf.save(update_fields=["status"])
                messages.success(request, f"Transfer {trf.transfer_reference} updated.")

        return redirect("logistics:warehouse_transfers_portal")

    transfers = WarehouseTransferProfile.objects.order_by("-created_at")[:50]
    return render(request, "logistics/warehouse_transfers.html", {
        "can_manage": can_manage,
        "transfers": transfers,
        "status_choices": WarehouseTransferProfile.TRANSFER_STATUS,
    })


@login_required
def logistics_returns_portal_view(request):
    """Manage return pickups and warehouse inspections."""
    can_manage = _can_manage_logistics(request.user)
    if request.method == "POST" and can_manage:
        action = request.POST.get("action")
        if action == "create_return":
            shipment_id = request.POST.get("shipment_id")
            ret_ref = request.POST.get("return_request_id", "").strip() or f"RET-{uuid.uuid4().hex[:8].upper()}"
            pickup_date = request.POST.get("pickup_date") or None
            shipment = get_object_or_404(ShipmentProfile, pk=shipment_id)
            try:
                LogisticsReturnProfile.objects.create(
                    return_request_id=ret_ref,
                    shipment=shipment,
                    status="pickup_scheduled",
                    pickup_date=pickup_date,
                )
                messages.success(request, f"Return pickup '{ret_ref}' scheduled.")
            except IntegrityError:
                messages.error(request, "Return request ID already exists.")

        elif action == "update_return":
            ret = get_object_or_404(LogisticsReturnProfile, pk=request.POST.get("return_id"))
            new_status = request.POST.get("status", "")
            if new_status in {c[0] for c in LogisticsReturnProfile.RETURN_STATUS}:
                ret.status = new_status
                ret.save(update_fields=["status"])
                messages.success(request, f"Return {ret.return_request_id} updated.")

        return redirect("logistics:logistics_returns_portal")

    returns = LogisticsReturnProfile.objects.select_related("shipment").order_by("-created_at")[:50]
    shipments = ShipmentProfile.objects.order_by("-created_at")[:50]
    return render(request, "logistics/logistics_returns.html", {
        "can_manage": can_manage,
        "returns": returns,
        "shipments": shipments,
        "status_choices": LogisticsReturnProfile.RETURN_STATUS,
    })
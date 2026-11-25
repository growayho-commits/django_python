import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.finances.payment_gateways.models.gateway_profile import EscrowTransaction
from apps.marketing_leads.customer_leads.models.lead_profile import CustomerLeadProfile
from apps.marketing_leads.orders.models.order_profile import OrderItem, OrderProfile
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
from apps.systems.audits.models.audit_profile import AuditLogProfile
from apps.systems.integrations.models.integration_profile import IntegrationProfile
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.models.role_upgrade_request import RoleUpgradeRequest
from apps.users.superusers.services.role_request_service import get_user_current_role

CoreUser = get_user_model()


def _can_access_systems(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "systems" in activities
    return False


def _answer_copilot_query(query: str, metrics: dict) -> str:
    q = (query or "").lower()
    if not q:
        return ""
    if "revenue" in q or "sales" in q or "order" in q:
        return (
            f"Total Orders: {metrics['total_orders']} | "
            f"Total Revenue: INR {metrics['total_revenue']} | "
            f"Escrow Held: INR {metrics['escrow_held']}."
        )
    if "pending" in q or "approval" in q:
        return (
            f"Pending Approvals — Catalogues: {metrics['pending_catalogues']}, "
            f"Service Providers: {metrics['pending_services']}, "
            f"Role Requests: {metrics['pending_roles']}."
        )
    if "fraud" in q or "alert" in q or "audit" in q:
        return (
            f"High-Value Orders (> INR 50,000): {metrics['high_value_orders']} | "
            f"Recent Audit Logs: {metrics['audit_count']}."
        )
    return (
        f"Platform Snapshot — Users: {metrics['total_users']}, "
        f"Approved Catalogues: {metrics['approved_catalogues']}, "
        f"Approved Services: {metrics['approved_services']}, "
        f"Orders: {metrics['total_orders']} (INR {metrics['total_revenue']})."
    )


@login_required
def systems_command_center_view(request):
    """Analytics, Demand Forecasting, AI Copilot, Audit/Fraud Alerts & External Integrations."""
    if not _can_access_systems(request.user):
        messages.error(request, "Permission denied. Systems access required.")
        return redirect("users:role_dashboard_redirect")

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_integration":
            service_name = request.POST.get("service_name", "").strip()
            webhook_url = request.POST.get("webhook_url", "").strip()
            api_key = request.POST.get("api_key", "").strip()
            if service_name:
                try:
                    IntegrationProfile.objects.create(
                        service_name=service_name,
                        webhook_url=webhook_url or None,
                        api_key=api_key or None,
                        is_active=True,
                    )
                    AuditLogProfile.objects.create(
                        user=request.user,
                        action="CREATE",
                        module_name="Integrations",
                        description=f"Added integration '{service_name}'.",
                        ip_address=request.META.get("REMOTE_ADDR"),
                    )
                    messages.success(request, f"Integration '{service_name}' added.")
                except IntegrityError:
                    messages.error(request, f"Integration '{service_name}' already exists.")

        elif action == "toggle_integration":
            integ = get_object_or_404(IntegrationProfile, pk=request.POST.get("integration_id"))
            integ.is_active = not integ.is_active
            integ.save(update_fields=["is_active"])
            messages.info(request, f"Integration '{integ.service_name}' updated.")

        return redirect("systems:command_center")

    last_30_days = timezone.now() - timedelta(days=30)
    total_revenue = OrderProfile.objects.aggregate(s=Sum("total_amount"))["s"] or 0
    escrow_held = EscrowTransaction.objects.filter(escrow_status="held").aggregate(s=Sum("amount"))["s"] or 0
    high_value_orders = OrderProfile.objects.filter(total_amount__gte=50000).count()

    metrics = {
        "total_users": CoreUser.objects.count(),
        "approved_catalogues": CoreCatalogProfile.objects.filter(approval_status="approved").count(),
        "approved_services": ProfessionalProfile.objects.filter(approval_status="approved").count(),
        "total_orders": OrderProfile.objects.count(),
        "total_revenue": total_revenue,
        "escrow_held": escrow_held,
        "pending_catalogues": CoreCatalogProfile.objects.filter(approval_status="pending").count(),
        "pending_services": ProfessionalProfile.objects.filter(approval_status="pending").count(),
        "pending_roles": RoleUpgradeRequest.objects.filter(status="pending").count(),
        "high_value_orders": high_value_orders,
        "audit_count": AuditLogProfile.objects.count(),
    }

    # Simple 30-day Demand Forecast by top ordered catalogues
    top_items = (
        OrderItem.objects.filter(catalogue__isnull=False, order__created_at__gte=last_30_days)
        .values("catalogue__name", "catalogue__sku")
        .annotate(units_sold=Sum("quantity"), order_count=Count("order", distinct=True))
        .order_by("-units_sold")[:10]
    )
    forecast_rows = [
        {
            "name": row["catalogue__name"],
            "sku": row["catalogue__sku"],
            "units_30d": row["units_sold"] or 0,
            "projected_next_30d": int((row["units_sold"] or 0) * 1.15) + 1,
            "orders": row["order_count"],
        }
        for row in top_items
    ]

    copilot_query = request.GET.get("copilot_q", "").strip()
    copilot_answer = _answer_copilot_query(copilot_query, metrics)

    audit_logs = AuditLogProfile.objects.select_related("user").order_by("-created_at")[:25]
    integrations = IntegrationProfile.objects.order_by("-created_at")
    feed_url = request.build_absolute_uri("/api/v1/systems/portal/external-feed/")
    enquiry_url = request.build_absolute_uri("/api/v1/systems/portal/external-enquiry/")

    return render(request, "systems/command_center.html", {
        "metrics": metrics,
        "forecast_rows": forecast_rows,
        "copilot_query": copilot_query,
        "copilot_answer": copilot_answer,
        "audit_logs": audit_logs,
        "integrations": integrations,
        "feed_url": feed_url,
        "enquiry_url": enquiry_url,
    })


def external_catalogue_feed_view(request):
    """Public JSON feed of approved Catalogues & Services for External Website sync."""
    catalogues = [
        {
            "id": c.id,
            "name": c.name,
            "sku": c.sku,
            "trade_channel": c.trade_channel,
            "base_price": str(c.base_price),
            "delivery_scope": c.delivery_scope,
        }
        for c in CoreCatalogProfile.objects.filter(approval_status="approved", is_active=True)[:100]
    ]
    services = [
        {
            "id": s.id,
            "skill_title": s.skill_title,
            "starting_fee": str(s.starting_fee),
            "delivery_scope": s.delivery_scope,
            "is_verified": s.is_verified,
        }
        for s in ProfessionalProfile.objects.filter(approval_status="approved")[:100]
    ]
    return JsonResponse({"status": "ok", "catalogues": catalogues, "services": services})


@csrf_exempt
def external_enquiry_webhook_view(request):
    """Receive Two-Way External Website enquiries into CustomerLeadProfile."""
    if request.method != "POST":
        return JsonResponse({"error": "POST method required"}, status=405)

    try:
        payload = json.loads(request.body.decode("utf-8")) if request.content_type == "application/json" else request.POST
    except Exception:
        payload = request.POST

    full_name = (payload.get("full_name") or "External Visitor").strip()
    email = (payload.get("email") or "").strip()
    phone = (payload.get("phone_number") or "").strip()
    notes = (payload.get("notes") or "").strip()

    if not email:
        return JsonResponse({"error": "email is required"}, status=400)

    lead = CustomerLeadProfile.objects.create(
        full_name=full_name,
        email=email,
        phone_number=phone,
        notes=notes,
        status="new",
        source="External Website",
    )
    AuditLogProfile.objects.create(
        action="EXTERNAL_LEAD",
        module_name="Integrations",
        description=f"External website enquiry #{lead.id} from {email}.",
        ip_address=request.META.get("REMOTE_ADDR"),
    )
    return JsonResponse({"status": "received", "lead_id": lead.id}, status=201)


def pwa_manifest_view(request):
    """Mobile PWA Manifest JSON."""
    return JsonResponse({
        "name": "Hybrid Marketplace",
        "short_name": "HybridMkt",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#0f172a",
        "theme_color": "#f59e0b",
        "icons": [],
    })


def pwa_service_worker_view(request):
    """Minimal PWA Service Worker."""
    js = "self.addEventListener('install', () => self.skipWaiting());\nself.addEventListener('fetch', () => {});"
    return HttpResponse(js, content_type="application/javascript")
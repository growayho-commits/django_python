from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.marketing_leads.customer_leads.models.lead_profile import CustomerLeadProfile
from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def _can_manage_all_leads(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "marketing_leads" in activities
    return False


@login_required
def rfq_leads_view(request):
    """Submit B2B RFQ quotes and manage incoming customer leads."""
    can_manage_all = _can_manage_all_leads(request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "submit_rfq":
            catalogue_id = request.POST.get("catalogue_id") or None
            catalogue = CoreCatalogProfile.objects.filter(pk=catalogue_id).first() if catalogue_id else None
            full_name = request.POST.get("full_name", "").strip() or (request.user.get_full_name() or request.user.email)
            email = request.POST.get("email", "").strip() or request.user.email
            phone = request.POST.get("phone_number", "").strip() or getattr(request.user, "phone_number", "")
            qty = max(1, int(request.POST.get("requested_quantity") or 1))
            target_price = request.POST.get("target_unit_price") or None
            notes = request.POST.get("notes", "").strip()

            lead = CustomerLeadProfile.objects.create(
                user=request.user,
                catalogue=catalogue,
                full_name=full_name,
                email=email,
                phone_number=phone,
                requested_quantity=qty,
                target_unit_price=target_price,
                notes=notes,
                status="new",
                source="B2B RFQ",
            )
            if catalogue and catalogue.owner and catalogue.owner_id != request.user.id:
                PushNotificationProfile.objects.create(
                    user=catalogue.owner,
                    title=f"New B2B RFQ for {catalogue.name}",
                    message=f"{full_name} requested a quote for {qty} units of '{catalogue.name}'.",
                )
            messages.success(request, f"RFQ #{lead.id} submitted successfully.")

        elif action == "update_status":
            lead = get_object_or_404(CustomerLeadProfile, pk=request.POST.get("lead_id"))
            is_cat_owner = lead.catalogue and lead.catalogue.owner_id == request.user.id
            if can_manage_all or is_cat_owner:
                new_status = request.POST.get("status", "")
                if new_status in {c[0] for c in CustomerLeadProfile.STATUS_CHOICES}:
                    lead.status = new_status
                    lead.save(update_fields=["status"])
                    if lead.user:
                        PushNotificationProfile.objects.create(
                            user=lead.user,
                            title=f"RFQ #{lead.id} Status Updated",
                            message=f"Your quote request status is now '{lead.get_status_display()}'.",
                        )
                    messages.success(request, f"Lead #{lead.id} marked as {lead.get_status_display()}.")

        return redirect("customer_leads:rfq_leads")

    my_rfqs = CustomerLeadProfile.objects.filter(user=request.user).select_related("catalogue").order_by("-created_at")
    if can_manage_all:
        incoming_leads = CustomerLeadProfile.objects.select_related("catalogue").order_by("-created_at")
    else:
        incoming_leads = CustomerLeadProfile.objects.filter(catalogue__owner=request.user).select_related("catalogue").order_by("-created_at")

    catalogues = CoreCatalogProfile.objects.filter(approval_status="approved", is_active=True).order_by("name")

    return render(request, "customer_leads/rfq_leads.html", {
        "my_rfqs": my_rfqs,
        "incoming_leads": incoming_leads,
        "catalogues": catalogues,
        "status_choices": CustomerLeadProfile.STATUS_CHOICES,
        "can_manage_all": can_manage_all,
    })
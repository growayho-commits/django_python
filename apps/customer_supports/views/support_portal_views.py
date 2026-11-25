from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.customer_supports.faqs.models.faq_profile import FAQProfile
from apps.customer_supports.helpdesk_tickets.models.ticket_profile import HelpdeskTicket
from apps.customer_supports.live_chats.models.chat_profile import LiveChatMessage
from apps.customer_supports.return_refunds.models.refund_profile import ReturnRefundProfile
from apps.marketing_leads.orders.models.order_profile import OrderProfile
from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role

CoreUser = get_user_model()


def _can_manage_support(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "customer_supports" in activities
    return False


@login_required
def support_portal_view(request):
    """Unified Customer Support Portal: FAQs, Helpdesk Tickets, Live Chat & Return/Refund Approvals."""
    can_manage = _can_manage_support(request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_ticket":
            subject = request.POST.get("subject", "").strip()
            priority = request.POST.get("priority", "Medium")
            description = request.POST.get("description", "").strip()
            if subject and description:
                ticket = HelpdeskTicket.objects.create(
                    user=request.user,
                    subject=subject,
                    priority=priority,
                    description=description,
                    status="Open",
                )
                messages.success(request, f"Support Ticket #{ticket.id} created.")

        elif action == "update_ticket" and can_manage:
            ticket = get_object_or_404(HelpdeskTicket, pk=request.POST.get("ticket_id"))
            new_status = request.POST.get("status", "Open")
            if new_status in {c[0] for c in HelpdeskTicket.STATUS_CHOICES}:
                ticket.status = new_status
                ticket.save(update_fields=["status"])
                PushNotificationProfile.objects.create(
                    user=ticket.user,
                    title=f"Ticket #{ticket.id} Updated",
                    message=f"Your ticket '{ticket.subject}' is now {new_status}.",
                )
                messages.success(request, f"Ticket #{ticket.id} marked {new_status}.")

        elif action == "create_refund":
            order_ref = request.POST.get("order_ref", "").strip()
            reason = request.POST.get("reason", "Defective")
            refund_amount = request.POST.get("refund_amount") or 0
            description = request.POST.get("description", "").strip()
            if order_ref and description:
                ReturnRefundProfile.objects.create(
                    user=request.user,
                    order=order_ref,
                    reason=reason,
                    refund_amount=refund_amount,
                    description=description,
                    status="Pending",
                )
                messages.success(request, f"Return/Refund request submitted for {order_ref}.")

        elif action == "moderate_refund" and can_manage:
            refund = get_object_or_404(ReturnRefundProfile, pk=request.POST.get("refund_id"))
            new_status = request.POST.get("status", "Pending")
            if new_status in {c[0] for c in ReturnRefundProfile.STATUS_CHOICES}:
                refund.status = new_status
                refund.admin_notes = request.POST.get("admin_notes", "").strip()
                refund.save(update_fields=["status", "admin_notes"])
                PushNotificationProfile.objects.create(
                    user=refund.user,
                    title=f"Refund Request {new_status}",
                    message=f"Your refund request for Order {refund.order} is now {new_status}.",
                )
                messages.success(request, f"Refund #{refund.id} marked {new_status}.")

        elif action == "send_chat":
            msg = request.POST.get("message", "").strip()
            receiver_email = request.POST.get("receiver_email", "").strip()
            receiver = CoreUser.objects.filter(email__iexact=receiver_email).first() if receiver_email else None
            if not receiver and not can_manage:
                receiver = CoreUser.objects.filter(is_superuser=True).order_by("id").first()
            if msg:
                LiveChatMessage.objects.create(
                    sender=request.user,
                    receiver=receiver,
                    message=msg,
                )
                messages.success(request, "Chat message sent.")

        elif action == "create_faq" and can_manage:
            question = request.POST.get("question", "").strip()
            answer = request.POST.get("answer", "").strip()
            if question and answer:
                FAQProfile.objects.create(question=question, answer=answer, is_active=True)
                messages.success(request, "FAQ added.")

        return redirect("customer_supports:support_portal")

    if can_manage:
        tickets = HelpdeskTicket.objects.select_related("user").order_by("-created_at")[:50]
        refunds = ReturnRefundProfile.objects.select_related("user").order_by("-created_at")[:50]
        chats = LiveChatMessage.objects.select_related("sender", "receiver").order_by("-timestamp")[:40]
    else:
        tickets = HelpdeskTicket.objects.filter(user=request.user).order_by("-created_at")[:30]
        refunds = ReturnRefundProfile.objects.filter(user=request.user).order_by("-created_at")[:30]
        chats = LiveChatMessage.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).select_related("sender", "receiver").order_by("-timestamp")[:40]

    faqs = FAQProfile.objects.filter(is_active=True).order_by("-created_at")
    user_orders = OrderProfile.objects.filter(user=request.user).order_by("-created_at")[:20]

    return render(request, "customer_supports/support_portal.html", {
        "can_manage": can_manage,
        "tickets": tickets,
        "refunds": refunds,
        "chats": chats,
        "faqs": faqs,
        "user_orders": user_orders,
        "ticket_priorities": HelpdeskTicket.PRIORITY_CHOICES,
        "ticket_statuses": HelpdeskTicket.STATUS_CHOICES,
        "refund_reasons": ReturnRefundProfile.REASON_CHOICES,
        "refund_statuses": ReturnRefundProfile.STATUS_CHOICES,
    })
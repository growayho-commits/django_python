from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile
from apps.users.superusers.services.role_request_service import get_user_current_role

CoreUser = get_user_model()


@login_required
def notifications_inbox_view(request):
    """View personal & broadcast notifications, mark read, and allow Superuser/Executive broadcast."""
    can_broadcast = request.user.is_superuser or get_user_current_role(request.user) == "executive"

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "mark_read":
            notif = get_object_or_404(PushNotificationProfile, pk=request.POST.get("notif_id"), user=request.user)
            notif.is_read = True
            notif.save(update_fields=["is_read"])

        elif action == "mark_all_read":
            PushNotificationProfile.objects.filter(user=request.user, is_read=False).update(is_read=True)
            messages.success(request, "All personal notifications marked as read.")

        elif action == "send_notification" and can_broadcast:
            title = request.POST.get("title", "").strip()
            message = request.POST.get("message", "").strip()
            recipient_email = request.POST.get("recipient_email", "").strip()
            recipient = CoreUser.objects.filter(email__iexact=recipient_email).first() if recipient_email else None

            if title and message:
                PushNotificationProfile.objects.create(
                    user=recipient,
                    title=title,
                    message=message,
                )
                messages.success(request, "Notification sent successfully.")

        return redirect("push_notifications:notifications_inbox")

    notifications = PushNotificationProfile.objects.filter(
        Q(user=request.user) | Q(user__isnull=True)
    ).order_by("-sent_at")

    return render(request, "push_notifications/notifications_inbox.html", {
        "notifications": notifications,
        "can_broadcast": can_broadcast,
    })
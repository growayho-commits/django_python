from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.common.location_service import LocationCoverageService
from apps.marketing_leads.push_notifications.models.notification_profile import PushNotificationProfile
from apps.professional_network.enquiries.models.enquiry import SkillEnquiry
from apps.professional_network.profiles.models.availability import ProviderAvailability
from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile, SERVICE_SCOPE_CHOICES
from apps.professional_network.ratings.models.review import SkillRating
from apps.professional_network.service_categries.models.service_categries_model import ServiceCategory
from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def _can_approve_services(user) -> bool:
    if user.is_superuser:
        return True
    if get_user_current_role(user) == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])
        return "professional_network" in activities
    return False


@login_required
def service_directory_view(request):
    """IndiaMART-style Service-Only Marketplace filtered by category, verified badge, and 7 scopes + online."""
    search_query = request.GET.get("q", "").strip()
    category_id = request.GET.get("category") or None
    verified_only = request.GET.get("verified") == "1"
    pincode = request.GET.get("pincode", "").strip() or None
    taluk = request.GET.get("taluk", "").strip() or None
    district = request.GET.get("district", "").strip() or None
    state = request.GET.get("state", "").strip() or None
    online_only = request.GET.get("online") == "1"

    qs = ProfessionalProfile.objects.filter(approval_status="approved").select_related(
        "user", "service_category", "availability"
    )
    if search_query:
        qs = qs.filter(
            Q(skill_title__icontains=search_query)
            | Q(description__icontains=search_query)
            | Q(city__icontains=search_query)
        )
    if category_id:
        qs = qs.filter(service_category_id=category_id)
    if verified_only:
        qs = qs.filter(is_verified=True)
    if online_only:
        qs = qs.filter(delivery_scope="online")

    has_loc_filter = any([pincode, taluk, district, state])
    provider_cards = []
    for prof in qs.order_by("-is_verified", "-created_at"):
        if has_loc_filter and not LocationCoverageService.is_location_covered(
            scope=prof.delivery_scope,
            locations=prof.delivery_locations,
            pincode=pincode,
            taluk=taluk,
            district=district,
            state=state,
        ):
            continue

        avg_stars = prof.received_ratings.aggregate(avg=Avg("stars"))["avg"] or 0
        rating_count = prof.received_ratings.count()
        avail = getattr(prof, "availability", None)
        provider_cards.append({
            "profile": prof,
            "avg_stars": round(avg_stars, 1),
            "rating_count": rating_count,
            "availability": avail,
        })

    categories = ServiceCategory.objects.filter(is_active=True).order_by("name")
    return render(request, "professional_network/service_directory.html", {
        "provider_cards": provider_cards,
        "categories": categories,
        "filters": {
            "q": search_query,
            "category": category_id,
            "verified": verified_only,
            "online": online_only,
            "pincode": pincode or "",
            "taluk": taluk or "",
            "district": district or "",
            "state": state or "",
        },
    })


@login_required
def service_provider_detail_view(request, pk):
    """Service Provider detail page with Enquiry submission, Star Ratings, and Location Check."""
    prof = get_object_or_404(
        ProfessionalProfile.objects.select_related("user", "service_category", "availability"),
        pk=pk,
    )
    can_approve = _can_approve_services(request.user)
    if prof.approval_status != "approved" and prof.user_id != request.user.id and not can_approve:
        messages.error(request, "This service profile is awaiting approval.")
        return redirect("professional_network:service_directory")

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "send_enquiry":
            msg = request.POST.get("message", "").strip()
            if msg:
                enq = SkillEnquiry.objects.create(
                    sender=request.user,
                    provider_profile=prof,
                    message=msg,
                )
                if prof.user_id != request.user.id:
                    PushNotificationProfile.objects.create(
                        user=prof.user,
                        title=f"New Service Enquiry: {prof.skill_title}",
                        message=f"{request.user.email} sent an enquiry (#{enq.id}).",
                    )
                messages.success(request, "Your service enquiry has been sent!")

        elif action == "submit_rating":
            enquiry_id = request.POST.get("enquiry_id")
            stars = max(1, min(5, int(request.POST.get("stars") or 5)))
            feedback = request.POST.get("feedback", "").strip()
            enq = SkillEnquiry.objects.filter(pk=enquiry_id, sender=request.user, provider_profile=prof).first()
            if enq and not hasattr(enq, "rating"):
                SkillRating.objects.create(
                    enquiry=enq,
                    customer=request.user,
                    provider_profile=prof,
                    stars=stars,
                    feedback=feedback,
                )
                messages.success(request, f"Thank you! {stars}-star rating submitted.")
            else:
                messages.error(request, "Send an enquiry first (or rating already submitted for this enquiry).")

        return redirect("professional_network:service_provider_detail", pk=prof.pk)

    ratings = prof.received_ratings.select_related("customer").order_by("-created_at")
    avg_stars = ratings.aggregate(avg=Avg("stars"))["avg"] or 0
    unrated_enquiries = SkillEnquiry.objects.filter(
        sender=request.user,
        provider_profile=prof,
        rating__isnull=True,
    ).order_by("-created_at")

    return render(request, "professional_network/service_provider_detail.html", {
        "prof": prof,
        "ratings": ratings,
        "avg_stars": round(avg_stars, 1),
        "rating_count": ratings.count(),
        "unrated_enquiries": unrated_enquiries,
    })


@login_required
def service_workspace_view(request):
    """
    Open to ALL users to register as a Service Provider (pending Superuser/Executive approval),
    manage Availability & Enquiries, and for Superuser/Executive to approve/verify providers.
    """
    can_approve = _can_approve_services(request.user)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "create_service":
            skill_title = request.POST.get("skill_title", "").strip()
            category_id = request.POST.get("service_category_id") or None
            hsn_code = request.POST.get("hsn_service_code", "").strip()
            description = request.POST.get("description", "").strip()
            exp_years = max(0, int(request.POST.get("experience_years") or 0))
            starting_fee = request.POST.get("starting_fee") or 0
            city = request.POST.get("city", "").strip()
            pincode = request.POST.get("pincode", "").strip()
            scope = request.POST.get("delivery_scope", "district")
            raw_locs = request.POST.get("delivery_locations_text", "")
            locs = [loc.strip() for loc in raw_locs.split(",") if loc.strip()]

            if skill_title and description:
                prof = ProfessionalProfile.objects.create(
                    user=request.user,
                    service_category=ServiceCategory.objects.filter(pk=category_id).first() if category_id else None,
                    skill_title=skill_title,
                    hsn_service_code=hsn_code,
                    description=description,
                    experience_years=exp_years,
                    starting_fee=starting_fee,
                    city=city,
                    pincode=pincode,
                    delivery_scope=scope,
                    delivery_locations=locs,
                    approval_status="approved" if request.user.is_superuser else "pending",
                    is_verified=True if request.user.is_superuser else False,
                )
                ProviderAvailability.objects.get_or_create(profile=prof)
                messages.success(request, f"Service '{prof.skill_title}' submitted ({prof.get_approval_status_display()}).")

        elif action == "update_availability":
            prof = get_object_or_404(ProfessionalProfile, pk=request.POST.get("profile_id"), user=request.user)
            avail, _ = ProviderAvailability.objects.get_or_create(profile=prof)
            avail.is_available = bool(request.POST.get("is_available"))
            avail.is_on_leave = bool(request.POST.get("is_on_leave"))
            avail.working_hours = request.POST.get("working_hours", "9:00 AM - 6:00 PM").strip()
            avail.save()
            messages.success(request, f"Availability updated for '{prof.skill_title}'.")

        elif action == "moderate_provider" and can_approve:
            prof = get_object_or_404(ProfessionalProfile, pk=request.POST.get("profile_id"))
            new_status = request.POST.get("approval_status")
            if new_status in {"approved", "rejected", "pending"}:
                prof.approval_status = new_status
                if new_status == "approved" and request.POST.get("verify_badge") == "1":
                    prof.is_verified = True
                prof.save(update_fields=["approval_status", "is_verified"])
                PushNotificationProfile.objects.create(
                    user=prof.user,
                    title=f"Service Profile {new_status.title()}",
                    message=f"Your service '{prof.skill_title}' is now {new_status.title()}.",
                )
                messages.success(request, f"Service '{prof.skill_title}' marked {new_status}.")

        elif action == "toggle_verified" and can_approve:
            prof = get_object_or_404(ProfessionalProfile, pk=request.POST.get("profile_id"))
            prof.is_verified = not prof.is_verified
            prof.save(update_fields=["is_verified"])
            messages.info(request, f"Verified badge updated for '{prof.skill_title}'.")

        return redirect("professional_network:service_workspace")

    my_services = ProfessionalProfile.objects.filter(user=request.user).select_related("availability", "service_category").order_by("-created_at")
    received_enquiries = SkillEnquiry.objects.filter(provider_profile__user=request.user).select_related("sender", "provider_profile").order_by("-created_at")
    all_services = (
        ProfessionalProfile.objects.select_related("user", "service_category", "availability").order_by("-created_at")
        if can_approve else []
    )

    return render(request, "professional_network/service_workspace.html", {
        "can_approve": can_approve,
        "my_services": my_services,
        "received_enquiries": received_enquiries,
        "all_services": all_services,
        "categories": ServiceCategory.objects.filter(is_active=True).order_by("name"),
        "geo_scopes": SERVICE_SCOPE_CHOICES,
    })
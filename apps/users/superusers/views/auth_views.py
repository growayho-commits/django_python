from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from apps.users.members.models import MemberProfile
from apps.users.sellers.models import SellerProfile
from apps.users.superusers.forms.core_users_forms import (
    GuestLoginForm,
    GuestRegisterForm,
    InAccountRegisterForm,
)
from apps.users.superusers.services.role_request_service import get_user_current_role
from .superuser_views import get_user_dashboard_url

CoreUser = get_user_model()


def _apply_registration_links(new_user, referrer=None):
    """
    Defaults new user to Member. Sets referred_by as reference for all roles,
    and auto-assigns MemberProfile.assigned_seller ONLY when referrer is a Seller.
    """
    member_profile, _ = MemberProfile.objects.get_or_create(user=new_user)
    if referrer and referrer.pk != new_user.pk:
        new_user.referred_by = referrer
        new_user.save(update_fields=['referred_by'])

        if get_user_current_role(referrer) == 'seller':
            seller_profile = SellerProfile.objects.filter(user=referrer).first()
            if seller_profile:
                member_profile.assigned_seller = seller_profile
                member_profile.save(update_fields=['assigned_seller'])


def guest_home_view(request):
    catalogues = []
    services = []
    service_categories = []
    providers = []
    try:
        from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
        qs = CoreCatalogProfile.objects.filter(is_active=True, approval_status='approved').order_by('-created_at')
        if not qs.exists():
            qs = CoreCatalogProfile.objects.filter(is_active=True).order_by('-created_at')
        catalogues = list(qs[:12])
    except Exception:
        pass
    try:
        from apps.professional_network.service_categries.models.service_categries_model import ServiceCategory, ServiceListing
        services = list(ServiceListing.objects.select_related('category').order_by('-created_at')[:6])
        service_categories = list(ServiceCategory.objects.filter(is_active=True, parent__isnull=True)[:6])
    except Exception:
        pass
    try:
        from apps.professional_network.profiles.models.skill_profile import ProfessionalProfile
        providers = list(ProfessionalProfile.objects.select_related('availability').order_by('-id')[:6])
    except Exception:
        pass
    return render(request, 'superusers/guest_home.html', {
        'catalogues': catalogues,
        'services': services,
        'service_categories': service_categories,
        'providers': providers,
    })


@transaction.atomic
def register_view(request):
    """Supports Mode 1 (Direct Registration) & Mode 2 (Referral Link Registration via ?ref=)."""
    if request.user.is_authenticated:
        return redirect('users:role_dashboard_redirect')

    ref_code = request.GET.get('ref', '').strip()
    if request.method == 'POST':
        form = GuestRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            submitted_ref = form.cleaned_data.get('referral_code', '').strip() or ref_code
            referrer = CoreUser.objects.filter(referral_code__iexact=submitted_ref).first() if submitted_ref else None
            _apply_registration_links(user, referrer=referrer)
            login(request, user)
            request.session.set_expiry(0)
            return redirect('users:role_dashboard_redirect')
    else:
        form = GuestRegisterForm(initial={'referral_code': ref_code})

    return render(request, 'superusers/register.html', {'form': form, 'ref_code': ref_code})


@login_required
@transaction.atomic
def in_account_register_view(request):
    """Supports Mode 3 (In-Account Registration by any logged-in user without logging out)."""
    if request.method == 'POST':
        form = InAccountRegisterForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            _apply_registration_links(new_user, referrer=request.user)
            messages.success(request, f'User {new_user.email} registered successfully.')
            return redirect('users:network_tree')
    else:
        form = InAccountRegisterForm()

    return render(request, 'superusers/in_account_register.html', {
        'form': form,
        'dashboard_url': get_user_dashboard_url(request.user),
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('users:role_dashboard_redirect')

    if request.method == 'POST':
        form = GuestLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                request.session.set_expiry(0)
                return redirect('users:role_dashboard_redirect')
            form.add_error(None, 'Invalid email or password')
    else:
        form = GuestLoginForm()
    return render(request, 'superusers/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('users:login')
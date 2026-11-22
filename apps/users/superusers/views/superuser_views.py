from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import NoReverseMatch, reverse
from django.views.generic import TemplateView

from apps.users.superusers.models import RoleUpgradeRequest


def _has_profile(user, attr_name):
    try:
        return getattr(user, attr_name) is not None
    except Exception:
        return False


def _get_latest_approved_role(user):
    latest = (
        RoleUpgradeRequest.objects.filter(user=user, status='approved')
        .order_by('-updated_at', '-id')
        .first()
    )
    return latest.requested_role.lower() if latest and latest.requested_role else None


def _safe_reverse(url_candidates, fallback_url):
    for url_name in url_candidates:
        try:
            return reverse(url_name)
        except NoReverseMatch:
            continue
    return fallback_url


def get_user_dashboard_url(user):
    if user.is_superuser or user.is_staff or _has_profile(user, 'superuser_profile'):
        return _safe_reverse(['users:dashboard', 'users:users:dashboard'], '/api/v1/users/superusers/dashboard/')

    latest_role = _get_latest_approved_role(user)
    if latest_role == 'executive' and _has_profile(user, 'executive_profile'):
        return _safe_reverse(['executives:executive_dashboard', 'users:executives:overview'], '/api/v1/users/executives/executive-dashboard/')
    if latest_role == 'merchant' and _has_profile(user, 'merchant_profile'):
        return _safe_reverse(['merchant:overview', 'users:merchant:overview'], '/api/v1/users/merchant/overview/')
    if latest_role == 'seller' and _has_profile(user, 'seller_profile'):
        return _safe_reverse(['sellers:overview', 'users:sellers:overview'], '/api/v1/users/sellers/overview/')
    if latest_role == 'member':
        return _safe_reverse(['members:dashboard', 'users:members:dashboard'], '/api/v1/users/members/dashboard/')

    if _has_profile(user, 'executive_profile'):
        return _safe_reverse(['executives:executive_dashboard', 'users:executives:overview'], '/api/v1/users/executives/executive-dashboard/')
    if _has_profile(user, 'merchant_profile'):
        return _safe_reverse(['merchant:overview', 'users:merchant:overview'], '/api/v1/users/merchant/overview/')
    if _has_profile(user, 'seller_profile'):
        return _safe_reverse(['sellers:overview', 'users:sellers:overview'], '/api/v1/users/sellers/overview/')

    return _safe_reverse(['members:dashboard', 'users:members:dashboard'], '/api/v1/users/members/dashboard/')


@login_required
def role_dashboard_redirect(request):
    return redirect(get_user_dashboard_url(request.user))


@login_required
def dashboard_view(request):
    return render(request, 'superusers/dashboard.html')


class SuperuserProfileCreateOrUpdateView(LoginRequiredMixin, TemplateView):
    template_name = 'superusers/dashboard.html'


def _render_tab(request, tab_name):
    return render(request, 'superusers/dashboard.html', {'active_tab': tab_name})


@login_required
def overview_view(request):
    return _render_tab(request, 'overview')


@login_required
def products_view(request):
    return _render_tab(request, 'products')


@login_required
def inventory_view(request):
    return _render_tab(request, 'inventory')


@login_required
def orders_view(request):
    return _render_tab(request, 'orders')


@login_required
def payouts_view(request):
    return _render_tab(request, 'payouts')


@login_required
def support_view(request):
    return _render_tab(request, 'support')


@login_required
def profile_view(request):
    return _render_tab(request, 'profile')
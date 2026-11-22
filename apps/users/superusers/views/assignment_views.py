from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from apps.users.executives.models import ExecutiveProfile
from apps.users.members.models import MemberProfile
from apps.users.merchant.models import MerchantProfile
from apps.users.sellers.models import SellerProfile
from apps.users.superusers.constants import EXECUTIVE_DEPARTMENTS
from apps.users.superusers.permissions import superuser_required
from apps.users.superusers.services.role_request_service import get_user_current_role


@login_required
@superuser_required
def manage_assignments_view(request):
    """
    Superuser hierarchy assignment view:
    - Add, edit, or remove Executive department activities (multi-select)
    - Assign/unassign Sellers to Executives
    - Assign/unassign Merchants to Executives
    - Assign/unassign Members to Sellers
    """
    department_choices = (
        list(EXECUTIVE_DEPARTMENTS.items())
        if isinstance(EXECUTIVE_DEPARTMENTS, dict)
        else list(EXECUTIVE_DEPARTMENTS)
    )
    valid_dept_keys = {key for key, _ in department_choices}

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'assign_executive_activities':
            exec_id = request.POST.get('executive_id')
            exec_profile = get_object_or_404(ExecutiveProfile, pk=exec_id)
            selected_activities = [
                key for key in request.POST.getlist('activities')
                if key in valid_dept_keys
            ]
            exec_profile.assigned_activities = selected_activities
            exec_profile.save(update_fields=['assigned_activities'])
            messages.success(request, f'Updated department activities for {exec_profile.user.email}.')

        elif action == 'clear_executive_activities':
            exec_id = request.POST.get('executive_id')
            exec_profile = get_object_or_404(ExecutiveProfile, pk=exec_id)
            exec_profile.assigned_activities = []
            exec_profile.save(update_fields=['assigned_activities'])
            messages.success(request, f'Cleared all department activities for {exec_profile.user.email}.')

        elif action == 'assign_seller_executive':
            seller_id = request.POST.get('seller_id')
            executive_profile_id = request.POST.get('executive_id') or None
            seller_profile = get_object_or_404(SellerProfile, pk=seller_id)
            seller_profile.assigned_executive_id = executive_profile_id
            seller_profile.save(update_fields=['assigned_executive'])
            messages.success(request, f'Updated assigned executive for seller {seller_profile.user.email}.')

        elif action == 'assign_merchant_executive':
            merchant_id = request.POST.get('merchant_id')
            executive_profile_id = request.POST.get('executive_id') or None
            merchant_profile = get_object_or_404(MerchantProfile, pk=merchant_id)
            merchant_profile.assigned_executive_id = executive_profile_id
            merchant_profile.save(update_fields=['assigned_executive'])
            messages.success(request, f'Updated assigned executive for merchant {merchant_profile.user.email}.')

        elif action == 'assign_member_seller':
            member_id = request.POST.get('member_id')
            seller_profile_id = request.POST.get('seller_id') or None
            member_profile = get_object_or_404(MemberProfile, pk=member_id)
            member_profile.assigned_seller_id = seller_profile_id
            member_profile.save(update_fields=['assigned_seller'])
            messages.success(request, f'Updated assigned seller for member {member_profile.user.email}.')

        return redirect('users:manage_assignments')

    executives = []
    for profile in ExecutiveProfile.objects.select_related('user').order_by('user__email'):
        if get_user_current_role(profile.user) == 'executive':
            profile.current_activities = list(profile.assigned_activities or [])
            executives.append(profile)

    sellers = [
        profile
        for profile in SellerProfile.objects.select_related('user', 'assigned_executive__user').order_by('user__email')
        if get_user_current_role(profile.user) == 'seller'
    ]
    merchants = [
        profile
        for profile in MerchantProfile.objects.select_related('user', 'assigned_executive__user').order_by('user__email')
        if get_user_current_role(profile.user) == 'merchant'
    ]
    members = [
        profile
        for profile in MemberProfile.objects.select_related('user', 'assigned_seller__user').filter(is_active_member=True).order_by('user__email')
        if get_user_current_role(profile.user) == 'member'
    ]

    context = {
        'executives': executives,
        'sellers': sellers,
        'merchants': merchants,
        'members': members,
        'departments': department_choices,
    }
    return render(request, 'superusers/manage_assignments.html', context)
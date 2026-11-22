from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from apps.users.executives.models import ExecutiveProfile
from apps.users.members.models import MemberProfile
from apps.users.merchant.models import MerchantProfile
from apps.users.sellers.models import SellerProfile
from apps.users.superusers.services.role_request_service import get_user_current_role

CoreUser = get_user_model()


def _serialize_user_node(user, role_label=None, extra_info="", children=None):
    """Build a dictionary node for the org-chart tree and detail modal."""
    resolved_role = role_label or (get_user_current_role(user) or "member")
    full_name = ""
    ind_profile = getattr(user, "individual_profile", None)
    if ind_profile:
        full_name = f"{getattr(ind_profile, 'first_name', '')} {getattr(ind_profile, 'last_name', '')}".strip()

    return {
        "id": user.id,
        "email": user.email,
        "full_name": full_name or user.email,
        "phone_number": getattr(user, "phone_number", "") or "N/A",
        "role": resolved_role.title(),
        "role_key": resolved_role.lower(),
        "referral_code": getattr(user, "referral_code", "") or "N/A",
        "referred_by": user.referred_by.email if getattr(user, "referred_by", None) else "Direct / None",
        "is_verified": "Verified" if getattr(user, "is_verified", False) else "Pending Verification",
        "date_joined": user.date_joined.strftime("%d %b %Y") if getattr(user, "date_joined", None) else "N/A",
        "extra_info": extra_info,
        "children": children or [],
    }


@login_required
def network_tree_view(request):
    """
    Centralized Role-Based Org-Chart Tree & Referral Network view:
    - Superuser: Full tree (Executives -> Sellers/Merchants -> Members)
    - Executive: Upward (Superuser) + Downward (Assigned Sellers -> Members, Assigned Merchants)
    - Seller: Upward (Assigned Executive) + Downward (Assigned Members)
    - Merchant: Upward (Assigned Executive), no downward assigned users
    - Member: Upward (Assigned Seller), no downward assigned users
    - All roles: Personal Referred-By list + copyable referral link
    """
    current_user = request.user
    current_role = (get_user_current_role(current_user) or "member").lower()

    tree_roots = []
    upward_user = None

    if current_role == "superuser" or current_user.is_superuser:
        executives = [
            p for p in ExecutiveProfile.objects.select_related("user").order_by("user__email")
            if get_user_current_role(p.user) == "executive"
        ]
        all_sellers = [
            p for p in SellerProfile.objects.select_related("user", "assigned_executive").order_by("user__email")
            if get_user_current_role(p.user) == "seller"
        ]
        all_merchants = [
            p for p in MerchantProfile.objects.select_related("user", "assigned_executive").order_by("user__email")
            if get_user_current_role(p.user) == "merchant"
        ]
        all_members = [
            p for p in MemberProfile.objects.select_related("user", "assigned_seller").filter(is_active_member=True).order_by("user__email")
            if get_user_current_role(p.user) == "member"
        ]

        exec_children_map = {ep.id: [] for ep in executives}
        seller_children_map = {sp.id: [] for sp in all_sellers}

        unassigned_members = []
        for mp in all_members:
            m_node = _serialize_user_node(mp.user, "member", f"Tier: {mp.get_membership_tier_display()}")
            if mp.assigned_seller_id and mp.assigned_seller_id in seller_children_map:
                seller_children_map[mp.assigned_seller_id].append(m_node)
            else:
                unassigned_members.append(m_node)

        unassigned_sellers = []
        for sp in all_sellers:
            s_node = _serialize_user_node(
                sp.user,
                "seller",
                f"Store: {sp.store_name or 'N/A'}",
                children=seller_children_map.get(sp.id, []),
            )
            if sp.assigned_executive_id and sp.assigned_executive_id in exec_children_map:
                exec_children_map[sp.assigned_executive_id].append(s_node)
            else:
                unassigned_sellers.append(s_node)

        unassigned_merchants = []
        for mrp in all_merchants:
            mr_node = _serialize_user_node(
                mrp.user,
                "merchant",
                f"Business: {mrp.business_name or 'N/A'}",
            )
            if mrp.assigned_executive_id and mrp.assigned_executive_id in exec_children_map:
                exec_children_map[mrp.assigned_executive_id].append(mr_node)
            else:
                unassigned_merchants.append(mr_node)

        exec_nodes = []
        for ep in executives:
            activities = ", ".join(getattr(ep, "assigned_activities", []) or []) or "No activities"
            exec_nodes.append(
                _serialize_user_node(
                    ep.user,
                    "executive",
                    f"Departments: {activities}",
                    children=exec_children_map.get(ep.id, []),
                )
            )

        root_children = exec_nodes + unassigned_sellers + unassigned_merchants + unassigned_members
        tree_roots = [
            _serialize_user_node(current_user, "superuser", "Platform Owner", children=root_children)
        ]

    elif current_role == "executive":
        owner = CoreUser.objects.filter(is_superuser=True).order_by("id").first()
        if owner:
            upward_user = _serialize_user_node(owner, "superuser", "Platform Owner")

        exec_profile = ExecutiveProfile.objects.filter(user=current_user).first()
        assigned_sellers = (
            [
                p for p in SellerProfile.objects.select_related("user").filter(assigned_executive=exec_profile)
                if get_user_current_role(p.user) == "seller"
            ]
            if exec_profile else []
        )
        assigned_merchants = (
            [
                p for p in MerchantProfile.objects.select_related("user").filter(assigned_executive=exec_profile)
                if get_user_current_role(p.user) == "merchant"
            ]
            if exec_profile else []
        )

        seller_nodes = []
        for sp in assigned_sellers:
            down_members = [
                _serialize_user_node(mp.user, "member", f"Tier: {mp.get_membership_tier_display()}")
                for mp in MemberProfile.objects.select_related("user").filter(assigned_seller=sp, is_active_member=True)
                if get_user_current_role(mp.user) == "member"
            ]
            seller_nodes.append(
                _serialize_user_node(sp.user, "seller", f"Store: {sp.store_name or 'N/A'}", children=down_members)
            )

        merchant_nodes = [
            _serialize_user_node(mrp.user, "merchant", f"Business: {mrp.business_name or 'N/A'}")
            for mrp in assigned_merchants
        ]

        activities = ", ".join(getattr(exec_profile, "assigned_activities", []) or []) or "No activities"
        tree_roots = [
            _serialize_user_node(
                current_user,
                "executive",
                f"Departments: {activities}",
                children=seller_nodes + merchant_nodes,
            )
        ]

    elif current_role == "seller":
        seller_profile = SellerProfile.objects.select_related("assigned_executive__user").filter(user=current_user).first()
        if seller_profile and seller_profile.assigned_executive:
            upward_user = _serialize_user_node(
                seller_profile.assigned_executive.user,
                "executive",
                "Assigned Executive",
            )

        down_members = (
            [
                _serialize_user_node(mp.user, "member", f"Tier: {mp.get_membership_tier_display()}")
                for mp in MemberProfile.objects.select_related("user").filter(assigned_seller=seller_profile, is_active_member=True)
                if get_user_current_role(mp.user) == "member"
            ]
            if seller_profile else []
        )
        tree_roots = [
            _serialize_user_node(
                current_user,
                "seller",
                f"Store: {getattr(seller_profile, 'store_name', '') or 'N/A'}",
                children=down_members,
            )
        ]

    elif current_role == "merchant":
        merchant_profile = MerchantProfile.objects.select_related("assigned_executive__user").filter(user=current_user).first()
        if merchant_profile and merchant_profile.assigned_executive:
            upward_user = _serialize_user_node(
                merchant_profile.assigned_executive.user,
                "executive",
                "Assigned Executive",
            )

    elif current_role == "member":
        member_profile = MemberProfile.objects.select_related("assigned_seller__user").filter(user=current_user).first()
        if member_profile and member_profile.assigned_seller:
            upward_user = _serialize_user_node(
                member_profile.assigned_seller.user,
                "seller",
                "Assigned Seller",
            )

    referred_users_qs = CoreUser.objects.filter(referred_by=current_user).order_by("-date_joined")
    referred_users = [_serialize_user_node(u) for u in referred_users_qs]

    referral_code = getattr(current_user, "referral_code", "") or ""
    referral_link = (
        request.build_absolute_uri(f"{reverse('users:register')}?ref={referral_code}")
        if referral_code
        else ""
    )

    context = {
        "current_role": current_role,
        "upward_user": upward_user,
        "tree_roots": tree_roots,
        "referred_users": referred_users,
        "referral_code": referral_code,
        "referral_link": referral_link,
    }
    return render(request, "superusers/network_tree.html", context)
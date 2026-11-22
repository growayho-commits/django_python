from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def executive_navigation_context(request):
    """Role-based 3-dot navigation menu for Executives."""
    if not request.user.is_authenticated or request.user.is_superuser:
        return {}

    current_role = (get_user_current_role(request.user) or "").lower()
    if current_role != "executive":
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    exec_profile = ExecutiveProfile.objects.filter(user=request.user).first()
    activities = set(getattr(exec_profile, "assigned_activities", []) or [])

    common_sub_apps = [
        {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
        {"title": "Executive Dashboard", "url": "/api/v1/users/executives/dashboard/"},
        {"title": "Executive Profile", "url": "/api/v1/users/executives/profile/"},
        {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
        {"title": "Register New User", "url": "/api/v1/users/superusers/in-account-register/"},
        {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
    ]

    if "merchant" in activities:
        common_sub_apps.append({"title": "Merchants Portal", "url": "/api/v1/users/merchant/overview/"})
    if "marketing_leads" in activities:
        common_sub_apps.append({"title": "Sellers Portal", "url": "/api/v1/users/sellers/overview/"})

    enterprise_modules = [
        {
            "id": "subExecOperations",
            "name": "Executive Operations",
            "icon": "fa-briefcase",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Commissions", "url": "/api/v1/users/executives/commissions/"},
                {"title": "Field Inspections", "url": "/api/v1/users/executives/inspections/"},
                {"title": "Leads Management", "url": "/api/v1/users/executives/leads/"},
                {"title": "Reports", "url": "/api/v1/users/executives/reports/"},
                {"title": "Vendor Onboarding", "url": "/api/v1/users/executives/onboarding/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subUsers",
            "name": "Users & Governance",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted(common_sub_apps, key=lambda x: x["title"]),
        },
    ]

    if "catalogs" in activities:
        enterprise_modules.append({
            "id": "subCatalogs",
            "name": "Catalogs & Products",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Categories", "url": "/api/v1/catalogs/categories/"},
                {"title": "Core Catalogs", "url": "/api/v1/catalogs/core/"},
                {"title": "Inventories", "url": "/api/v1/catalogs/inventory/"},
            ], key=lambda x: x["title"]),
        })

    if "finances" in activities:
        enterprise_modules.append({
            "id": "subFinances",
            "name": "Finances & Banking",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": [{"title": "Finances Overview", "url": "/api/v1/finances/"}],
        })

    if "logistics" in activities:
        enterprise_modules.append({
            "id": "subLogistics",
            "name": "Logistics & Supply",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": [{"title": "Logistics & Shipments", "url": "/api/v1/logistics/"}],
        })

    if "marketing_leads" in activities:
        enterprise_modules.append({
            "id": "subMarketing",
            "name": "Marketing & Leads",
            "icon": "fa-bullhorn",
            "color": "amber",
            "sub_apps": [{"title": "Orders & Campaigns", "url": "/api/v1/marketing/orders/"}],
        })

    if "customer_supports" in activities:
        enterprise_modules.append({
            "id": "subSupport",
            "name": "Customer Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": [{"title": "Helpdesk Tickets", "url": "/api/v1/support/helpdesk-tickets/"}],
        })

    if "professional_network" in activities:
        enterprise_modules.append({
            "id": "subProfessional",
            "name": "Professional Network",
            "icon": "fa-user-tie",
            "color": "blue",
            "sub_apps": [{"title": "Professional Directory", "url": "/api/v1/professional-network/"}],
        })

    if "systems" in activities:
        enterprise_modules.append({
            "id": "subSystems",
            "name": "Systems & Analytics",
            "icon": "fa-server",
            "color": "teal",
            "sub_apps": [{"title": "System Analytics", "url": "/api/v1/systems/"}],
        })

    enterprise_modules = sorted(enterprise_modules, key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "executive",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
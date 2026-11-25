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

    if "merchants" in activities or "merchant" in activities:
        common_sub_apps.append({"title": "Merchants Portal", "url": "/api/v1/users/merchants/overview/"})
    if "marketing_leads" in activities:
        common_sub_apps.append({"title": "Sellers Portal", "url": "/api/v1/users/sellers/overview/"})

    enterprise_modules = [
        {
            "id": "subMarketplace",
            "name": "Catalogue Marketplace",
            "short_name": "Marketplace",
            "icon": "fa-store",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "Browse & Purchase Catalogues", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
                {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subExecOperations",
            "name": "Executive Operations",
            "short_name": "Operations",
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
            "short_name": "Users",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted(common_sub_apps, key=lambda x: x["title"]),
        },
    ]

    if "catalogs" in activities or "marketing_leads" in activities:
        enterprise_modules.append({
            "id": "subCatalogs",
            "name": "Catalogs & Approvals",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
                {"title": "Catalogue Workspace & Approvals", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
                {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
            ], key=lambda x: x["title"]),
        })

    if "finances" in activities:
        enterprise_modules.append({
            "id": "subFinances",
            "name": "Finances & Banking",
            "short_name": "Finances",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": [
                {"title": "Bank Accounts", "url": "/api/v1/finances/portal/bank-accounts/"},
                {"title": "Commissions & Payouts", "url": "/api/v1/finances/portal/payouts/"},
                {"title": "Escrow & Settlements", "url": "/api/v1/finances/portal/escrow/"},
                {"title": "In-House GST Invoices", "url": "/api/v1/finances/portal/gst-invoices/"},
            ],
        })

    if "logistics" in activities:
        enterprise_modules.append({
            "id": "subLogistics",
            "name": "Logistics & Supply",
            "short_name": "Logistics",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": [
                {"title": "Return Pickups", "url": "/api/v1/logistics/portal/returns/"},
                {"title": "Shipments & Live Tracking", "url": "/api/v1/logistics/portal/"},
                {"title": "Warehouse Transfers", "url": "/api/v1/logistics/portal/transfers/"},
            ],
        })

    if "marketing_leads" in activities:
        enterprise_modules.append({
            "id": "subMarketing",
            "name": "Marketing & Leads",
            "short_name": "Marketing",
            "icon": "fa-bullhorn",
            "color": "amber",
            "sub_apps": [
                {"title": "B2B RFQ & Customer Leads", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
                {"title": "Coupons & Discounts", "url": "/api/v1/marketing_leads/coupons_discounts/portal/"},
                {"title": "Orders & Fulfillment", "url": "/api/v1/marketing_leads/orders/my-orders/"},
                {"title": "Push Notifications", "url": "/api/v1/marketing_leads/push_notifications/portal/"},
            ],
        })

    if "customer_supports" in activities:
        enterprise_modules.append({
            "id": "subSupport",
            "name": "Customer Support",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": [{"title": "Support & Resolution Center", "url": "/api/v1/customer_supports/portal/"}],
        })

    if "professional_network" in activities:
        enterprise_modules.append({
            "id": "subProfessional",
            "name": "Professional Network",
            "short_name": "Professionals",
            "icon": "fa-user-tie",
            "color": "blue",
            "sub_apps": [
                {"title": "Provider Approvals & Workspace", "url": "/api/v1/professional_network/portal/workspace/"},
                {"title": "Service Directory", "url": "/api/v1/professional_network/portal/"},
            ],
        })

    if "systems" in activities:
        enterprise_modules.append({
            "id": "subSystems",
            "name": "Systems & AI Copilot",
            "short_name": "Systems",
            "icon": "fa-server",
            "color": "teal",
            "sub_apps": [{"title": "Systems Command Center", "url": "/api/v1/systems/portal/"}],
        })

    enterprise_modules = sorted(enterprise_modules, key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "executive",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
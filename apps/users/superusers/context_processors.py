from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def enterprise_navigation_context(request):
    """
    Dynamic role-based navigation context processor for the 3-dot menu
    and flyout submenus in base.html across all authenticated user roles.
    """
    if not request.user.is_authenticated:
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    user = request.user
    current_role = (get_user_current_role(user) or "member").lower()
    if user.is_superuser:
        current_role = "superuser"

    user_dashboard_url = get_user_dashboard_url(user)

    # Common features available to all authenticated users
    common_user_sub_apps = [
        {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
        {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
        {"title": "Register New User", "url": "/api/v1/users/superusers/in-account-register/"},
        {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
    ]

    catalogs_module = {
        "id": "subCatalogs",
        "name": "Catalogs & Products",
        "short_name": "Catalogs",
        "icon": "fa-boxes-stacked",
        "color": "indigo",
        "badge": "13 Sub-Apps",
        "status": "Synced",
        "description": "Attributes, Inventories & Master Catalogs",
        "main_url": "/api/v1/catalogs/",
        "sub_apps": sorted([
            {"title": "Attributes", "url": "/api/v1/catalogs/attributes/"},
            {"title": "Bundles & Kits", "url": "/api/v1/catalogs/bundles/"},
            {"title": "Catalog Medias", "url": "/api/v1/catalogs/media/"},
            {"title": "Catalog Statuses", "url": "/api/v1/catalogs/status/"},
            {"title": "Catalog Wishlist", "url": "/api/v1/catalogs/wishlist/"},
            {"title": "Categories", "url": "/api/v1/catalogs/categories/"},
            {"title": "Core Catalogs", "url": "/api/v1/catalogs/core/"},
            {"title": "Inventories", "url": "/api/v1/catalogs/inventory/"},
            {"title": "Pricing Tiers", "url": "/api/v1/catalogs/pricing/"},
            {"title": "Reviews & Ratings", "url": "/api/v1/catalogs/reviews/"},
            {"title": "Search Filters", "url": "/api/v1/catalogs/search-filters/"},
            {"title": "Specifications", "url": "/api/v1/catalogs/specifications/"},
            {"title": "Variants", "url": "/api/v1/catalogs/variants/"},
        ], key=lambda x: x["title"]),
    }

    support_module = {
        "id": "subSupport",
        "name": "Customer Support",
        "short_name": "Support",
        "icon": "fa-headset",
        "color": "sky",
        "badge": "Help Desk",
        "status": "Active",
        "description": "FAQs, Tickets, Live Chats & Refund Complaints",
        "main_url": "/api/v1/support/",
        "sub_apps": sorted([
            {"title": "FAQs", "url": "/api/v1/support/faqs/"},
            {"title": "Helpdesk Tickets", "url": "/api/v1/support/helpdesk-tickets/"},
            {"title": "Live Chats", "url": "/api/v1/support/live-chats/"},
            {"title": "Refunds & Complaints", "url": "/api/v1/support/return-refunds/"},
        ], key=lambda x: x["title"]),
    }

    finances_module = {
        "id": "subFinances",
        "name": "Finances & Banking",
        "short_name": "Finances",
        "icon": "fa-wallet",
        "color": "emerald",
        "badge": "Gateways",
        "status": "Secured",
        "description": "Accounts, Taxes, Commissions & Payouts",
        "main_url": "/api/v1/finances/",
        "sub_apps": sorted([
            {"title": "Bank Accounts", "url": "/api/v1/finances/"},
            {"title": "Commissions", "url": "/api/v1/finances/"},
            {"title": "Payment Gateways", "url": "/api/v1/finances/"},
            {"title": "Payouts", "url": "/api/v1/finances/"},
            {"title": "Taxes", "url": "/api/v1/finances/"},
        ], key=lambda x: x["title"]),
    }

    logistics_module = {
        "id": "subLogistics",
        "name": "Logistics & Supply",
        "short_name": "Logistics",
        "icon": "fa-truck-fast",
        "color": "purple",
        "badge": "Tracking",
        "status": "Live",
        "description": "Partners, Shipments & Warehouse Transfers",
        "main_url": "/api/v1/logistics/",
        "sub_apps": sorted([
            {"title": "Logistics Partners", "url": "/api/v1/logistics/"},
            {"title": "Returns & Tracking", "url": "/api/v1/logistics/"},
            {"title": "Shipments", "url": "/api/v1/logistics/"},
            {"title": "Warehouse Transfers", "url": "/api/v1/logistics/"},
        ], key=lambda x: x["title"]),
    }

    marketing_module = {
        "id": "subMarketing",
        "name": "Marketing & Leads",
        "short_name": "Marketing",
        "icon": "fa-bullhorn",
        "color": "amber",
        "badge": "Campaigns",
        "status": "Running",
        "description": "Ad Campaigns, Coupons, Orders & Leads",
        "main_url": "/api/v1/marketing/",
        "sub_apps": sorted([
            {"title": "Ad Campaigns", "url": "/api/v1/marketing/"},
            {"title": "Carts", "url": "/api/v1/marketing/carts/"},
            {"title": "Checkout Flows", "url": "/api/v1/marketing/checkout/"},
            {"title": "Coupons & Discounts", "url": "/api/v1/marketing/coupons/"},
            {"title": "Customer Leads", "url": "/api/v1/marketing/"},
            {"title": "Orders", "url": "/api/v1/marketing/orders/"},
            {"title": "Push Notifications", "url": "/api/v1/marketing/notifications/"},
            {"title": "Wishlists", "url": "/api/v1/marketing/wishlist/"},
        ], key=lambda x: x["title"]),
    }

    professional_module = {
        "id": "subProfessional",
        "name": "Professional Network",
        "short_name": "Professionals",
        "icon": "fa-user-tie",
        "color": "blue",
        "badge": "5 Sub-Apps",
        "status": "Active",
        "description": "Service Categories, Profiles, Enquiries & Search",
        "main_url": "/api/v1/professional-network/",
        "sub_apps": sorted([
            {"title": "Directory Search Engine", "url": "/api/v1/professional-network/"},
            {"title": "Professional Profiles", "url": "/api/v1/professional-network/"},
            {"title": "Ratings & Reviews", "url": "/api/v1/professional-network/"},
            {"title": "Service Categories", "url": "/api/v1/professional-network/"},
            {"title": "Skill Enquiries Inbox", "url": "/api/v1/professional-network/"},
        ], key=lambda x: x["title"]),
    }

    systems_module = {
        "id": "subSystems",
        "name": "Systems & Analytics",
        "short_name": "Systems",
        "icon": "fa-server",
        "color": "teal",
        "badge": "Monitoring",
        "status": "Healthy",
        "description": "Security Audits, ROI & API Integrations",
        "main_url": "/api/v1/systems/",
        "sub_apps": sorted([
            {"title": "Analytics & Forecasting", "url": "/api/v1/systems/"},
            {"title": "Integrations & AI Tools", "url": "/api/v1/systems/"},
            {"title": "Security Audits", "url": "/api/v1/systems/"},
        ], key=lambda x: x["title"]),
    }

    enterprise_modules = []

    if current_role == "superuser":
        users_sub_apps = common_user_sub_apps + [
            {"title": "Executives Management", "url": "/api/v1/users/executives/dashboard/"},
            {"title": "Manage Assignments", "url": "/api/v1/users/superusers/manage-assignments/"},
            {"title": "Manage Role Requests", "url": "/api/v1/users/superusers/manage-roles/"},
            {"title": "Members Portal", "url": "/api/v1/users/members/dashboard/"},
            {"title": "Merchants Portal", "url": "/api/v1/users/merchant/dashboard/"},
            {"title": "Sellers Portal", "url": "/api/v1/users/sellers/overview/"},
            {"title": "Superusers Dashboard", "url": "/api/v1/users/superusers/dashboard/"},
        ]
        enterprise_modules = [
            catalogs_module,
            support_module,
            finances_module,
            logistics_module,
            marketing_module,
            professional_module,
            systems_module,
            {
                "id": "subUsers",
                "name": "Users & Governance",
                "short_name": "Users",
                "icon": "fa-users-gear",
                "color": "rose",
                "badge": "Full Control",
                "status": "Restricted",
                "description": "Executives, Merchants, Sellers & Members",
                "main_url": "/api/v1/users/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    elif current_role == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])

        users_sub_apps = common_user_sub_apps + [
            {"title": "Executive Dashboard", "url": "/api/v1/users/executives/dashboard/"},
        ]
        if "merchant" in activities:
            users_sub_apps.append({"title": "Merchants Portal", "url": "/api/v1/users/merchant/dashboard/"})
        if "marketing_leads" in activities:
            users_sub_apps.append({"title": "Sellers Portal", "url": "/api/v1/users/sellers/overview/"})

        enterprise_modules.append({
            "id": "subUsers",
            "name": "Users & Governance",
            "short_name": "Users",
            "icon": "fa-users-gear",
            "color": "rose",
            "badge": "Executive",
            "status": "Active",
            "description": "Profile, Network Tree & Assigned Portals",
            "main_url": "/api/v1/users/executives/dashboard/",
            "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
        })

        if "catalogs" in activities:
            enterprise_modules.append(catalogs_module)
        if "customer_supports" in activities:
            enterprise_modules.append(support_module)
        if "finances" in activities:
            enterprise_modules.append(finances_module)
        if "logistics" in activities:
            enterprise_modules.append(logistics_module)
        if "marketing_leads" in activities:
            enterprise_modules.append(marketing_module)
        if "professional_network" in activities:
            enterprise_modules.append(professional_module)
        if "systems" in activities:
            enterprise_modules.append(systems_module)

    elif current_role == "seller":
        users_sub_apps = common_user_sub_apps + [
            {"title": "Seller Overview", "url": "/api/v1/users/sellers/overview/"},
            {"title": "Seller Dashboard", "url": "/api/v1/users/sellers/dashboard/"},
        ]
        enterprise_modules = [
            catalogs_module,
            support_module,
            finances_module,
            marketing_module,
            {
                "id": "subUsers",
                "name": "Users & Governance",
                "short_name": "Users",
                "icon": "fa-users-gear",
                "color": "rose",
                "badge": "Seller",
                "status": "Active",
                "description": "Profile, Network Tree & Seller Portal",
                "main_url": "/api/v1/users/sellers/overview/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    elif current_role == "merchant":
        users_sub_apps = common_user_sub_apps + [
            {"title": "Merchant Overview", "url": "/api/v1/users/merchant/overview/"},
            {"title": "Merchant Dashboard", "url": "/api/v1/users/merchant/dashboard/"},
        ]
        enterprise_modules = [
            catalogs_module,
            support_module,
            finances_module,
            marketing_module,
            {
                "id": "subUsers",
                "name": "Users & Governance",
                "short_name": "Users",
                "icon": "fa-users-gear",
                "color": "rose",
                "badge": "Merchant",
                "status": "Active",
                "description": "Profile, Network Tree & Merchant Portal",
                "main_url": "/api/v1/users/merchant/overview/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    else:  # member
        users_sub_apps = common_user_sub_apps + [
            {"title": "Member Dashboard", "url": "/api/v1/users/members/dashboard/"},
        ]
        enterprise_modules = [
            {
                "id": "subCatalogs",
                "name": "Catalogs & Products",
                "short_name": "Catalogs",
                "icon": "fa-boxes-stacked",
                "color": "indigo",
                "badge": "Browse",
                "status": "Active",
                "description": "Browse Marketplace Products & Wishlists",
                "main_url": "/api/v1/catalogs/core/",
                "sub_apps": [
                    {"title": "Browse Products", "url": "/api/v1/catalogs/core/"},
                    {"title": "Catalog Wishlist", "url": "/api/v1/catalogs/wishlist/"},
                ],
            },
            {
                "id": "subOrders",
                "name": "Orders & Shopping",
                "short_name": "Orders",
                "icon": "fa-cart-shopping",
                "color": "amber",
                "badge": "Buyer",
                "status": "Active",
                "description": "Carts, Checkout & My Orders",
                "main_url": "/api/v1/marketing/orders/",
                "sub_apps": [
                    {"title": "Carts", "url": "/api/v1/marketing/carts/"},
                    {"title": "My Orders", "url": "/api/v1/marketing/orders/"},
                    {"title": "Wishlists", "url": "/api/v1/marketing/wishlist/"},
                ],
            },
            support_module,
            {
                "id": "subUsers",
                "name": "Users & Governance",
                "short_name": "Users",
                "icon": "fa-users-gear",
                "color": "rose",
                "badge": "Member",
                "status": "Active",
                "description": "Profile, Referral Tree & Role Upgrade",
                "main_url": "/api/v1/users/members/dashboard/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    enterprise_modules = sorted(enterprise_modules, key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": current_role,
        "user_dashboard_url": user_dashboard_url,
    }
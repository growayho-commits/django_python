from apps.users.executives.models import ExecutiveProfile
from apps.users.superusers.services.role_request_service import get_user_current_role


def enterprise_navigation_context(request):
    """
    Dynamic role-based navigation context processor for the 3-dot menu,
    flyout submenus, and dashboard module cards across all user roles.
    """
    if not request.user.is_authenticated:
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    user = request.user
    current_role = (get_user_current_role(user) or "member").lower()
    if user.is_superuser:
        current_role = "superuser"

    user_dashboard_url = get_user_dashboard_url(user)

    common_user_sub_apps = [
        {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
        {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
        {"title": "Register New User", "url": "/api/v1/users/superusers/in-account-register/"},
        {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
    ]

    catalogs_module = {
        "id": "subCatalogs",
        "name": "Catalogs & Supply",
        "short_name": "Catalogs",
        "icon": "fa-boxes-stacked",
        "color": "indigo",
        "badge": "Portal",
        "status": "Synced",
        "description": "Catalogues, Categories, Bundles, Pricing & Wishlist",
        "main_url": "/api/v1/catalogs/core_catalogs/workspace/",
        "sub_apps": sorted([
            {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
            {"title": "Catalogue Marketplace", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
            {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
            {"title": "Catalogue Workspace", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
            {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
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
        "description": "FAQs, Tickets, Live Chats & Return/Refund Approvals",
        "main_url": "/api/v1/customer_supports/portal/",
        "sub_apps": [
            {"title": "Support & Resolution Center", "url": "/api/v1/customer_supports/portal/"},
        ],
    }

    finances_module = {
        "id": "subFinances",
        "name": "Finances & Banking",
        "short_name": "Finances",
        "icon": "fa-wallet",
        "color": "emerald",
        "badge": "Escrow & GST",
        "status": "Secured",
        "description": "Escrow, Commission Split, Wallet & 3-Type GST Invoices",
        "main_url": "/api/v1/finances/portal/escrow/",
        "sub_apps": sorted([
            {"title": "Bank Accounts", "url": "/api/v1/finances/portal/bank-accounts/"},
            {"title": "Commissions & Payouts", "url": "/api/v1/finances/portal/payouts/"},
            {"title": "Escrow & Settlements", "url": "/api/v1/finances/portal/escrow/"},
            {"title": "In-House GST Invoices", "url": "/api/v1/finances/portal/gst-invoices/"},
            {"title": "Referral & Loyalty Wallet", "url": "/api/v1/finances/portal/wallet/"},
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
        "description": "Shipments, Live Tracking, Transfers & Returns",
        "main_url": "/api/v1/logistics/portal/",
        "sub_apps": sorted([
            {"title": "Return Pickups", "url": "/api/v1/logistics/portal/returns/"},
            {"title": "Shipments & Live Tracking", "url": "/api/v1/logistics/portal/"},
            {"title": "Warehouse Transfers", "url": "/api/v1/logistics/portal/transfers/"},
        ], key=lambda x: x["title"]),
    }

    marketing_module = {
        "id": "subMarketing",
        "name": "Marketing & Orders",
        "short_name": "Orders",
        "icon": "fa-bullhorn",
        "color": "amber",
        "badge": "B2B & B2C",
        "status": "Running",
        "description": "Cart, Checkout, Orders, B2B RFQ, Coupons & Alerts",
        "main_url": "/api/v1/marketing_leads/orders/my-orders/",
        "sub_apps": sorted([
            {"title": "B2B RFQ & Customer Leads", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
            {"title": "Checkout", "url": "/api/v1/marketing_leads/checkout_flows/portal/"},
            {"title": "Coupons & Discounts", "url": "/api/v1/marketing_leads/coupons_discounts/portal/"},
            {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
            {"title": "Orders & Fulfillment", "url": "/api/v1/marketing_leads/orders/my-orders/"},
            {"title": "Push Notifications", "url": "/api/v1/marketing_leads/push_notifications/portal/"},
        ], key=lambda x: x["title"]),
    }

    professional_module = {
        "id": "subProfessional",
        "name": "Professional Network",
        "short_name": "Professionals",
        "icon": "fa-user-tie",
        "color": "blue",
        "badge": "Services",
        "status": "Active",
        "description": "IndiaMART-Style Service Directory & Provider Workspace",
        "main_url": "/api/v1/professional_network/portal/",
        "sub_apps": sorted([
            {"title": "Offer Service / Workspace", "url": "/api/v1/professional_network/portal/workspace/"},
            {"title": "Service Directory", "url": "/api/v1/professional_network/portal/"},
        ], key=lambda x: x["title"]),
    }

    systems_module = {
        "id": "subSystems",
        "name": "Systems & AI Copilot",
        "short_name": "Systems",
        "icon": "fa-server",
        "color": "teal",
        "badge": "AI & Audit",
        "status": "Healthy",
        "description": "Analytics, Demand Forecast, AI Copilot & External Sync",
        "main_url": "/api/v1/systems/portal/",
        "sub_apps": [
            {"title": "Systems Command Center", "url": "/api/v1/systems/portal/"},
        ],
    }

    enterprise_modules = []

    if current_role == "superuser":
        users_sub_apps = common_user_sub_apps + [
            {"title": "Executives Management", "url": "/api/v1/users/executives/dashboard/"},
            {"title": "Manage Assignments", "url": "/api/v1/users/superusers/manage-assignments/"},
            {"title": "Manage Role Requests", "url": "/api/v1/users/superusers/manage-roles/"},
            {"title": "Members Portal", "url": "/api/v1/users/members/dashboard/"},
            {"title": "Merchants Portal", "url": "/api/v1/users/merchants/overview/"},
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
                "main_url": "/api/v1/users/superusers/dashboard/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    elif current_role == "executive":
        exec_profile = ExecutiveProfile.objects.filter(user=user).first()
        activities = set(getattr(exec_profile, "assigned_activities", []) or [])

        users_sub_apps = common_user_sub_apps + [
            {"title": "Executive Dashboard", "url": "/api/v1/users/executives/dashboard/"},
        ]
        if "merchants" in activities or "merchant" in activities:
            users_sub_apps.append({"title": "Merchants Portal", "url": "/api/v1/users/merchants/overview/"})
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

        enterprise_modules.append({
            "id": "subMarketplace",
            "name": "Catalogue Marketplace",
            "short_name": "Marketplace",
            "icon": "fa-store",
            "color": "amber",
            "badge": "Buyer",
            "status": "Active",
            "description": "Browse & Purchase Approved Catalogues",
            "main_url": "/api/v1/catalogs/core_catalogs/marketplace/",
            "sub_apps": [
                {"title": "Browse Catalogues", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
                {"title": "My Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
            ],
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
            {"title": "Seller Profile", "url": "/api/v1/users/sellers/profile/"},
        ]
        seller_catalog_module = dict(catalogs_module)
        seller_catalog_module["sub_apps"] = sorted([
            {"title": "B2B Merchant Catalogues (Buy)", "url": "/api/v1/catalogs/core_catalogs/marketplace/?channel=b2b"},
            {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
            {"title": "Catalogue Marketplace", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
            {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
            {"title": "Catalogue Workspace (Manage)", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
            {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
        ], key=lambda x: x["title"])

        enterprise_modules = [
            seller_catalog_module,
            support_module,
            finances_module,
            logistics_module,
            marketing_module,
            professional_module,
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
            {"title": "Merchant Overview", "url": "/api/v1/users/merchants/overview/"},
            {"title": "Merchant Profile", "url": "/api/v1/users/merchants/profile/"},
        ]
        merchant_catalog_module = dict(catalogs_module)
        merchant_catalog_module["sub_apps"] = sorted([
            {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
            {"title": "Catalogue Marketplace (Buy)", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
            {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
            {"title": "Catalogue Workspace (Manage)", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
            {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
        ], key=lambda x: x["title"])

        enterprise_modules = [
            merchant_catalog_module,
            support_module,
            finances_module,
            logistics_module,
            marketing_module,
            professional_module,
            {
                "id": "subUsers",
                "name": "Users & Governance",
                "short_name": "Users",
                "icon": "fa-users-gear",
                "color": "rose",
                "badge": "Merchant",
                "status": "Active",
                "description": "Profile, Network Tree & Merchant Portal",
                "main_url": "/api/v1/users/merchants/overview/",
                "sub_apps": sorted(users_sub_apps, key=lambda x: x["title"]),
            },
        ]

    else:  # member
        users_sub_apps = common_user_sub_apps + [
            {"title": "Member Dashboard", "url": "/api/v1/users/members/dashboard/"},
            {"title": "Member Profile", "url": "/api/v1/users/members/profile/"},
        ]
        enterprise_modules = [
            {
                "id": "subCatalogs",
                "name": "Catalogs & Supply",
                "short_name": "Catalogs",
                "icon": "fa-boxes-stacked",
                "color": "indigo",
                "badge": "Browse",
                "status": "Active",
                "description": "Browse Marketplace Catalogues & Wishlists",
                "main_url": "/api/v1/catalogs/core_catalogs/marketplace/",
                "sub_apps": [
                    {"title": "Browse Catalogues", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                    {"title": "My Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
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
                "description": "Cart, Checkout, Orders & Notifications",
                "main_url": "/api/v1/marketing_leads/orders/my-orders/",
                "sub_apps": [
                    {"title": "B2B RFQ Quotes", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
                    {"title": "Checkout", "url": "/api/v1/marketing_leads/checkout_flows/portal/"},
                    {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
                    {"title": "My Orders", "url": "/api/v1/marketing_leads/orders/my-orders/"},
                    {"title": "Notifications Inbox", "url": "/api/v1/marketing_leads/push_notifications/portal/"},
                ],
            },
            support_module,
            professional_module,
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
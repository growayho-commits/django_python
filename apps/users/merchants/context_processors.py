from apps.users.superusers.services.role_request_service import get_user_current_role


def merchants_navigation_context(request):
    """Role-based 3-dot navigation menu for Merchants."""
    if not request.user.is_authenticated or request.user.is_superuser:
        return {}

    current_role = (get_user_current_role(request.user) or "").lower()
    if current_role != "merchant":
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    enterprise_modules = sorted([
        {
            "id": "subCatalogs",
            "name": "Catalogs & B2B Supply",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
                {"title": "Catalogue Marketplace (Buy)", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
                {"title": "Catalogue Workspace (Manage)", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
                {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
                {"title": "Merchant Catalogs", "url": "/api/v1/users/merchants/catalogs/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subFinances",
            "name": "Finances & Banking",
            "short_name": "Finances",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": sorted([
                {"title": "Bank Accounts", "url": "/api/v1/finances/portal/bank-accounts/"},
                {"title": "Commissions & Payouts", "url": "/api/v1/finances/portal/payouts/"},
                {"title": "Escrow & Settlements", "url": "/api/v1/finances/portal/escrow/"},
                {"title": "In-House GST Invoices", "url": "/api/v1/finances/portal/gst-invoices/"},
                {"title": "Merchant Finances", "url": "/api/v1/users/merchants/finances/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subLogistics",
            "name": "Logistics & Supply",
            "short_name": "Logistics",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": sorted([
                {"title": "Merchant Logistics", "url": "/api/v1/users/merchants/logistics/"},
                {"title": "Return Pickups", "url": "/api/v1/logistics/portal/returns/"},
                {"title": "Shipments & Live Tracking", "url": "/api/v1/logistics/portal/"},
                {"title": "Warehouse Transfers", "url": "/api/v1/logistics/portal/transfers/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subOrders",
            "name": "Orders & B2B RFQ",
            "short_name": "Orders",
            "icon": "fa-cart-shopping",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "B2B RFQ & Customer Leads", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
                {"title": "Merchant Orders", "url": "/api/v1/users/merchants/orders/"},
                {"title": "Merchant Overview", "url": "/api/v1/users/merchants/overview/"},
                {"title": "Orders & Fulfillment", "url": "/api/v1/marketing_leads/orders/my-orders/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subProfessional",
            "name": "Professional Services",
            "short_name": "Services",
            "icon": "fa-user-tie",
            "color": "blue",
            "sub_apps": sorted([
                {"title": "Offer Service / Workspace", "url": "/api/v1/professional_network/portal/workspace/"},
                {"title": "Service Directory", "url": "/api/v1/professional_network/portal/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subSupport",
            "name": "Customer Support",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": [
                {"title": "Support & Resolution Center", "url": "/api/v1/customer_supports/portal/"},
            ],
        },
        {
            "id": "subUsers",
            "name": "Users & Governance",
            "short_name": "Users",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted([
                {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
                {"title": "Merchant Business Profile", "url": "/api/v1/users/merchants/profile/"},
                {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
                {"title": "Register New User", "url": "/api/v1/users/superusers/in-account-register/"},
                {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
            ], key=lambda x: x["title"]),
        },
    ], key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "merchant",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
from apps.users.superusers.services.role_request_service import get_user_current_role


def seller_navigation_context(request):
    """
    Role-based 3-dot menu and right-side flyout submenu navigation
    tailored specifically for Seller activities.
    """
    if not request.user.is_authenticated or request.user.is_superuser:
        return {}

    current_role = (get_user_current_role(request.user) or "").lower()
    if current_role != "seller":
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    enterprise_modules = sorted([
        {
            "id": "subCatalogs",
            "name": "Catalogs & Supply",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "B2B Merchant Catalogues (Buy)", "url": "/api/v1/catalogs/core_catalogs/marketplace/?channel=b2b"},
                {"title": "Bundles & Kits", "url": "/api/v1/catalogs/core_catalogs/bundles/"},
                {"title": "Catalogue Marketplace", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "Catalogue Workspace (Manage)", "url": "/api/v1/catalogs/core_catalogs/workspace/"},
                {"title": "Categories", "url": "/api/v1/catalogs/core_catalogs/categories/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subSupport",
            "name": "Customer Support",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": sorted([
                {"title": "Seller Support", "url": "/api/v1/users/sellers/support/"},
                {"title": "Support & Resolution Center", "url": "/api/v1/customer_supports/portal/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subFinances",
            "name": "Finances & Payouts",
            "short_name": "Finances",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": sorted([
                {"title": "Bank Accounts", "url": "/api/v1/finances/portal/bank-accounts/"},
                {"title": "Commissions & Payouts", "url": "/api/v1/finances/portal/payouts/"},
                {"title": "In-House GST Invoices", "url": "/api/v1/finances/portal/gst-invoices/"},
                {"title": "Referral & Loyalty Wallet", "url": "/api/v1/finances/portal/wallet/"},
                {"title": "Seller Payouts", "url": "/api/v1/users/sellers/payouts/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subInventory",
            "name": "Inventory & Logistics",
            "short_name": "Inventory",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": sorted([
                {"title": "Inventory & Stock", "url": "/api/v1/users/sellers/inventory/"},
                {"title": "Return Pickups", "url": "/api/v1/logistics/portal/returns/"},
                {"title": "Shipments & Live Tracking", "url": "/api/v1/logistics/portal/"},
                {"title": "Warehouse Transfers", "url": "/api/v1/logistics/portal/transfers/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subMarketing",
            "name": "Marketing & Buyer Mode",
            "short_name": "Marketing",
            "icon": "fa-bullhorn",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "B2B RFQ & Customer Leads", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
                {"title": "Browse & Buy Catalogues", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "Catalogue Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
                {"title": "Coupons & Discounts", "url": "/api/v1/marketing_leads/coupons_discounts/portal/"},
                {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
                {"title": "Notifications Inbox", "url": "/api/v1/marketing_leads/push_notifications/portal/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subOrders",
            "name": "Orders & Fulfillment",
            "short_name": "Orders",
            "icon": "fa-cart-shopping",
            "color": "blue",
            "sub_apps": sorted([
                {"title": "Orders & Fulfillment", "url": "/api/v1/marketing_leads/orders/my-orders/"},
                {"title": "Seller Orders", "url": "/api/v1/users/sellers/orders/"},
                {"title": "Seller Overview", "url": "/api/v1/users/sellers/overview/"},
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
            "id": "subUsers",
            "name": "Users & Governance",
            "short_name": "Users",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted([
                {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
                {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
                {"title": "Register New Member", "url": "/api/v1/users/superusers/in-account-register/"},
                {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
                {"title": "Seller Store Profile", "url": "/api/v1/users/sellers/profile/"},
            ], key=lambda x: x["title"]),
        },
    ], key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "seller",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
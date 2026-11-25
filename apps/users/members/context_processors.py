from apps.users.superusers.services.role_request_service import get_user_current_role


def member_navigation_context(request):
    """
    Role-based 3-dot menu and right-side white flyout submenu navigation
    tailored specifically for Member activities.
    """
    if not request.user.is_authenticated or request.user.is_superuser:
        return {}

    current_role = (get_user_current_role(request.user) or "member").lower()
    if current_role != "member":
        return {}

    from apps.users.superusers.views.superuser_views import get_user_dashboard_url

    enterprise_modules = sorted([
        {
            "id": "subCartCoupons",
            "name": "Cart & Coupons",
            "short_name": "Cart",
            "icon": "fa-bag-shopping",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "B2B RFQ Quotes", "url": "/api/v1/marketing_leads/customer_leads/portal/"},
                {"title": "Checkout", "url": "/api/v1/marketing_leads/checkout_flows/portal/"},
                {"title": "Coupons & Discounts", "url": "/api/v1/marketing_leads/coupons_discounts/portal/"},
                {"title": "My Cart", "url": "/api/v1/marketing_leads/carts/my-cart/"},
                {"title": "Notifications Inbox", "url": "/api/v1/marketing_leads/push_notifications/portal/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subCatalogs",
            "name": "Catalogs & Supply",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Browse Catalogues", "url": "/api/v1/catalogs/core_catalogs/marketplace/"},
                {"title": "Member Catalogs", "url": "/api/v1/users/members/catalogs/"},
                {"title": "My Wishlist", "url": "/api/v1/catalogs/core_catalogs/wishlist/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subSupport",
            "name": "Helpdesk & Live Chat",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": [
                {"title": "Support & Resolution Center", "url": "/api/v1/customer_supports/portal/"},
            ],
        },
        {
            "id": "subOrders",
            "name": "Orders & Live Tracking",
            "short_name": "Orders",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": sorted([
                {"title": "Marketplace Orders", "url": "/api/v1/marketing_leads/orders/my-orders/"},
                {"title": "My Orders", "url": "/api/v1/users/members/orders/"},
                {"title": "Shipments & Tracking", "url": "/api/v1/logistics/portal/"},
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
            "short_name": "Account",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted([
                {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
                {"title": "Member Dashboard", "url": "/api/v1/users/members/dashboard/"},
                {"title": "Member Profile", "url": "/api/v1/users/members/profile/"},
                {"title": "Network & Referral Tree", "url": "/api/v1/users/superusers/network-tree/"},
                {"title": "Register New User", "url": "/api/v1/users/superusers/in-account-register/"},
                {"title": "Role Upgrade Request", "url": "/api/v1/users/superusers/role-request/submit/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subFinances",
            "name": "Wallet, Bank & Taxes",
            "short_name": "Wallet",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": sorted([
                {"title": "Bank Accounts", "url": "/api/v1/finances/portal/bank-accounts/"},
                {"title": "In-House GST Invoices", "url": "/api/v1/finances/portal/gst-invoices/"},
                {"title": "Referral & Loyalty Wallet", "url": "/api/v1/finances/portal/wallet/"},
            ], key=lambda x: x["title"]),
        },
    ], key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "member",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
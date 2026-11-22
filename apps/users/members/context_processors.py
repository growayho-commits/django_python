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
                {"title": "Checkout Flow", "url": "/api/v1/marketing/checkout/"},
                {"title": "Coupons & Discounts", "url": "/api/v1/marketing/coupons/"},
                {"title": "My Cart", "url": "/api/v1/marketing/carts/"},
                {"title": "Saved Wishlists", "url": "/api/v1/marketing/wishlist/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subCatalogs",
            "name": "Catalogs & Products",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Browse Catalogs", "url": "/api/v1/users/members/catalogs/"},
                {"title": "Catalog Wishlist", "url": "/api/v1/catalogs/wishlist/"},
                {"title": "Categories", "url": "/api/v1/catalogs/categories/"},
                {"title": "Marketplace Products", "url": "/api/v1/catalogs/core/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subSupport",
            "name": "Helpdesk & Live Chat",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": sorted([
                {"title": "FAQs", "url": "/api/v1/support/faqs/"},
                {"title": "Helpdesk Tickets", "url": "/api/v1/support/helpdesk-tickets/"},
                {"title": "Live Chats", "url": "/api/v1/support/live-chats/"},
                {"title": "Refunds & Complaints", "url": "/api/v1/support/return-refunds/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subOrders",
            "name": "Orders & Live Tracking",
            "short_name": "Orders",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": sorted([
                {"title": "Marketplace Orders", "url": "/api/v1/marketing/orders/"},
                {"title": "My Orders", "url": "/api/v1/users/members/orders/"},
                {"title": "Returns & Tracking", "url": "/api/v1/logistics/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subProfessional",
            "name": "Professional Services",
            "short_name": "Services",
            "icon": "fa-user-tie",
            "color": "blue",
            "sub_apps": sorted([
                {"title": "Directory Search Engine", "url": "/api/v1/professional-network/"},
                {"title": "Professional Services", "url": "/api/v1/users/members/services/"},
                {"title": "Service Categories", "url": "/api/v1/professional-network/"},
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
                {"title": "Bank Accounts", "url": "/api/v1/finances/"},
                {"title": "Member Finances", "url": "/api/v1/users/members/finances/"},
                {"title": "Payment Gateways", "url": "/api/v1/finances/"},
                {"title": "Taxes & Invoices", "url": "/api/v1/finances/"},
            ], key=lambda x: x["title"]),
        },
    ], key=lambda x: x["name"])

    return {
        "enterprise_modules": enterprise_modules,
        "active_user_role": "member",
        "user_dashboard_url": get_user_dashboard_url(request.user),
    }
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
            "name": "Catalogs & Products",
            "short_name": "Catalogs",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Attributes & Variants", "url": "/api/v1/catalogs/variants/"},
                {"title": "Categories", "url": "/api/v1/catalogs/categories/"},
                {"title": "Marketplace Catalogs", "url": "/api/v1/catalogs/core/"},
                {"title": "My Products", "url": "/api/v1/users/sellers/products/"},
                {"title": "Pricing Tiers", "url": "/api/v1/catalogs/pricing/"},
                {"title": "Product Media", "url": "/api/v1/catalogs/media/"},
                {"title": "Reviews & Ratings", "url": "/api/v1/catalogs/reviews/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subSupport",
            "name": "Customer Support",
            "short_name": "Support",
            "icon": "fa-headset",
            "color": "sky",
            "sub_apps": sorted([
                {"title": "Helpdesk Tickets", "url": "/api/v1/support/helpdesk-tickets/"},
                {"title": "Return & Refund Complaints", "url": "/api/v1/support/return-refunds/"},
                {"title": "Seller Support", "url": "/api/v1/users/sellers/support/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subFinances",
            "name": "Finances & Payouts",
            "short_name": "Finances",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": sorted([
                {"title": "Bank Accounts & Taxes", "url": "/api/v1/finances/"},
                {"title": "Commissions", "url": "/api/v1/finances/"},
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
                {"title": "Catalog Inventories", "url": "/api/v1/catalogs/inventory/"},
                {"title": "Inventory & Stock", "url": "/api/v1/users/sellers/inventory/"},
                {"title": "Returns & Tracking", "url": "/api/v1/logistics/"},
                {"title": "Shipments & Dispatch", "url": "/api/v1/logistics/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subMarketing",
            "name": "Marketing & Buyer Mode",
            "short_name": "Marketing",
            "icon": "fa-bullhorn",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "Browse & Buy Products", "url": "/api/v1/catalogs/core/"},
                {"title": "Coupons & Discounts", "url": "/api/v1/marketing/coupons/"},
                {"title": "My Cart", "url": "/api/v1/marketing/carts/"},
                {"title": "Wishlist", "url": "/api/v1/catalogs/wishlist/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subOrders",
            "name": "Orders & Fulfillment",
            "short_name": "Orders",
            "icon": "fa-cart-shopping",
            "color": "blue",
            "sub_apps": sorted([
                {"title": "Marketplace Orders", "url": "/api/v1/marketing/orders/"},
                {"title": "Seller Orders", "url": "/api/v1/users/sellers/orders/"},
                {"title": "Seller Overview", "url": "/api/v1/users/sellers/overview/"},
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
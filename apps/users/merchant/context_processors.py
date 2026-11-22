from apps.users.superusers.services.role_request_service import get_user_current_role


def merchant_navigation_context(request):
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
            "name": "Catalogs & Bundles",
            "icon": "fa-boxes-stacked",
            "color": "indigo",
            "sub_apps": sorted([
                {"title": "Bundles & Kits", "url": "/api/v1/users/merchant/bundles/"},
                {"title": "Marketplace Catalogs", "url": "/api/v1/catalogs/core/"},
                {"title": "Merchant Catalogs", "url": "/api/v1/users/merchant/catalogs/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subFinances",
            "name": "Finances & Banking",
            "icon": "fa-wallet",
            "color": "emerald",
            "sub_apps": [
                {"title": "Merchant Finances", "url": "/api/v1/users/merchant/finances/"},
            ],
        },
        {
            "id": "subLogistics",
            "name": "Logistics & Supply",
            "icon": "fa-truck-fast",
            "color": "purple",
            "sub_apps": [
                {"title": "Merchant Logistics", "url": "/api/v1/users/merchant/logistics/"},
            ],
        },
        {
            "id": "subOrders",
            "name": "Orders & Overview",
            "icon": "fa-cart-shopping",
            "color": "amber",
            "sub_apps": sorted([
                {"title": "Merchant Orders", "url": "/api/v1/users/merchant/orders/"},
                {"title": "Merchant Overview", "url": "/api/v1/users/merchant/overview/"},
            ], key=lambda x: x["title"]),
        },
        {
            "id": "subUsers",
            "name": "Users & Governance",
            "icon": "fa-users-gear",
            "color": "rose",
            "sub_apps": sorted([
                {"title": "Common Profile & Address", "url": "/api/v1/users/superusers/common-profile/"},
                {"title": "Merchant Business Profile", "url": "/api/v1/users/merchant/profile/"},
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
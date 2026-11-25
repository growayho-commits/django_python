# App configuration
APP_CONFIG = {
    "app_path": "apps.users.merchants",
    "domain": "users",
    "name": "merchants",
    "title": "Merchants",
    "enabled": True,
    "role": "merchant",
    "dashboard_url": "/api/v1/users/merchants/overview/",
    "context_processor": "apps.users.merchants.context_processors.merchants_navigation_context",
}

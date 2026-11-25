# App configuration
APP_CONFIG = {
    "app_path": "apps.users.sellers",
    "domain": "users",
    "name": "sellers",
    "title": "Sellers",
    "enabled": True,
    "role": "seller",
    "dashboard_url": "/api/v1/users/sellers/overview/",
    "context_processor": "apps.users.sellers.context_processors.seller_navigation_context",
}

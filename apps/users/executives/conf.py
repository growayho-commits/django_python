# App configuration
APP_CONFIG = {
    "app_path": "apps.users.executives",
    "domain": "users",
    "name": "executives",
    "title": "Executives",
    "enabled": True,
    "role": "executive",
    "dashboard_url": "/api/v1/users/executives/dashboard/",
    "context_processor": "apps.users.executives.context_processors.executive_navigation_context",
}

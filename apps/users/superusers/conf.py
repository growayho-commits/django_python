# App configuration
APP_CONFIG = {
    "app_path": "apps.users.superusers",
    "domain": "users",
    "name": "superusers",
    "title": "Superusers",
    "enabled": True,
    "role": "superuser",
    "dashboard_url": "/api/v1/users/superusers/dashboard/",
    "context_processor": "apps.users.superusers.context_processors.enterprise_navigation_context",
}

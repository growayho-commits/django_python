# App configuration
APP_CONFIG = {
    "app_path": "apps.users.members",
    "domain": "users",
    "name": "members",
    "title": "Members",
    "enabled": True,
    "role": "member",
    "dashboard_url": "/api/v1/users/members/dashboard/",
    "context_processor": "apps.users.members.context_processors.member_navigation_context",
}

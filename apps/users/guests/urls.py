from django.urls import path
from apps.users.guests.views.core_users_views import (
    register_view,
    login_view,
    logout_view,
    role_dashboard_redirect,
)

app_name = 'guests'

urlpatterns = [
    path('registration/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('role-redirect/', role_dashboard_redirect, name='role_dashboard_redirect'),
]
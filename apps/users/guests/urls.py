from django.urls import path
from apps.users.guests.views.core_users_views import (
    register_view,
    login_view,
    logout_view,
    role_dashboard_redirect,
    guest_home_view,
)

app_name = 'guests'

urlpatterns = [
    # இந்தப் பாதை உள்ளதா என்பதைச் சரிபார்க்கவும்:
    path('', guest_home_view, name='guest_home'),
    path('registration/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('role-redirect/', role_dashboard_redirect, name='role_dashboard_redirect'),
]
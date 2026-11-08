from django.urls import path
from apps.users.superusers.views import role_views, superuser_views
from apps.users.superusers.views.superuser_views import (
    guest_home_view, 
    login_view, 
    register_view, 
    logout_view, 
    role_dashboard_redirect, 
    superuser_dashboard_view
)

app_name = 'superusers'

urlpatterns = [
    # முகப்பு மற்றும் அங்கீகாரம் (Auth & Home)
    path('', guest_home_view, name='guest_home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('role-redirect/', role_dashboard_redirect, name='role-redirect'),

    # சூப்பர்யூசர் சுயவிவரம் மற்றும் டேஷ்போர்ட்
    path('profile/', superuser_views.SuperuserProfileCreateOrUpdateView.as_view(), name='profile'),
    path('dashboard/', superuser_dashboard_view, name='dashboard'), # அல்லது சூப்பர்யூசர் வியூ தேவைக்கேற்ப

    # ரோல் மேனேஜ்மென்ட் (Role Management)
    path('roles/manage/', role_views.manage_roles_view, name='manage_roles'),
    path('roles/assign/', role_views.assign_role_view, name='assign_role'),
    path('roles/toggle/<int:assignment_id>/', role_views.toggle_role_status_view, name='toggle_role_status'),
]
from django.urls import path
from apps.users.guests.views.guest_views import guest_home_view
from apps.users.guests.views.core_users_views import login_view, register_view, logout_view

urlpatterns = [
    path('', guest_home_view, name='guest_home'),
    path('registration/', register_view, name='registration'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
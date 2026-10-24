from django.urls import path
from apps.users.core_users.views.guest_views import guest_home_view

urlpatterns = [
    path('', guest_home_view, name='guest_home'),
]

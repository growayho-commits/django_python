from django.urls import path
from apps.users.superusers.views import superuser_views

app_name = 'superusers'

urlpatterns = [
    path('profile/', superuser_views.SuperuserProfileCreateOrUpdateView.as_view(), name='profile'),
    path('dashboard/', superuser_views.SuperuserProfileCreateOrUpdateView.as_view(), name='dashboard'),
]
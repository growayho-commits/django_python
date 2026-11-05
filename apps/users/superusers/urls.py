from django.urls import path
from apps.users.superusers.views import superuser_views

app_name = 'superusers'

urlpatterns = [
    path('dashboard/', superuser_views.superuser_dashboard, name='dashboard'),
    path('profile/', superuser_views.SuperuserProfileCreateOrUpdateView.as_view(), name='profile'),
]
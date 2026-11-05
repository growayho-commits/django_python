from django.urls import path
from apps.users.executives.views import executive_views

app_name = 'executives'

urlpatterns = [
    path('dashboard/', executive_views.executive_dashboard, name='dashboard'),
    path('profile/', executive_views.ExecutiveProfileCreateOrUpdateView.as_view(), name='profile'),
]
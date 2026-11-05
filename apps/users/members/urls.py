from django.urls import path
from apps.users.members.views.member_views import member_dashboard_view, MemberProfileCreateOrUpdateView

app_name = 'members'

urlpatterns = [
    path('dashboard/', member_dashboard_view, name='dashboard'),
    path('profile/', MemberProfileCreateOrUpdateView.as_view(), name='member-profile'),
]
from django.urls import path
from apps.users.members.views import MemberProfileCreateOrUpdateView

urlpatterns = [
    path('profile/', MemberProfileCreateOrUpdateView.as_view(), name='member-profile'),
]
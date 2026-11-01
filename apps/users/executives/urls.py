from django.urls import path
from apps.users.executives.views import ExecutiveProfileCreateOrUpdateView

urlpatterns = [
    path('profile/', ExecutiveProfileCreateOrUpdateView.as_view(), name='executive-profile'),
]
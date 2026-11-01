from django.urls import path
from apps.professional_network.profiles.views import create_profile_view, update_availability_view

app_name = 'profiles'

urlpatterns = [
    path('create/', create_profile_view, name='create_profile'),
    path('schedule/<int:profile_id>/', update_availability_view, name='update_schedule'),
]
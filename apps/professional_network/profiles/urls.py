from django.urls import path
from .views.leave_management import update_availability_view
from .views.profile_create import create_profile_view

app_name = 'profiles'

urlpatterns = [
    path('update-availability/', update_availability_view, name='update_availability'),
    path('create-profile/', create_profile_view, name='create_profile'),
]

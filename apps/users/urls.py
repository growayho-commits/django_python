from django.urls import path, include

urlpatterns = [
    path('guests/', include('apps.users.guests.urls')),
    path('superusers/', include('apps.users.superusers.urls')),
]
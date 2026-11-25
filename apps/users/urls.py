from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('members/', include('apps.users.members.urls')),
    path('superusers/', include('apps.users.superusers.urls')),
    path('executives/', include('apps.users.executives.urls')),
    path('merchants/', include('apps.users.merchants.urls')),
    path('sellers/', include('apps.users.sellers.urls')),
]

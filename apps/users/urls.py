from django.urls import path, include

app_name = 'users'

urlpatterns = [
    path('members/', include('apps.users.members.urls')),
    path('superusers/', include('apps.users.superusers.urls')),
    path('executives/', include('apps.users.executives.urls')),
    path('merchant/', include('apps.users.merchant.urls')),
    path('sellers/', include('apps.users.sellers.urls')),
]

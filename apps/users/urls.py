from django.urls import path, include

urlpatterns = [
    
    path('members/', include(('apps.users.members.urls', 'members'), namespace='members')),
    path('merchant/', include(('apps.users.merchant.urls', 'merchant'), namespace='merchant')),
    path('executives/', include(('apps.users.executives.urls', 'executives'), namespace='executives')),
    path('sellers/', include(('apps.users.sellers.urls', 'sellers'), namespace='sellers')),
    #path('superusers/', include(('apps.users.superusers.urls', 'superusers'), namespace='superusers')),
]
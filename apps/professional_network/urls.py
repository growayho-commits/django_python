from django.urls import path, include

app_name = 'professional_network'

urlpatterns = [
    path('profiles/', include('apps.professional_network.profiles.urls')),
    path('search/', include('apps.professional_network.search_engine.urls')),
    path('enquiries/', include('apps.professional_network.enquiries.urls')),
    path('ratings/', include('apps.professional_network.ratings.urls')),
    path('services/', include('apps.professional_network.service_categries.urls')),
]
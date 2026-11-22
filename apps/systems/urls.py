from django.urls import path, include

app_name = 'systems'

urlpatterns = [
    path('analytics/', include('apps.systems.analytics.urls')),
    path('audits/', include('apps.systems.audits.urls')),
    path('integrations/', include('apps.systems.integrations.urls')),
]

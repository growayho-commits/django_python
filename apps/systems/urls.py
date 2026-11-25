from django.urls import include, path

from apps.systems.views.systems_portal_views import (
    external_catalogue_feed_view,
    external_enquiry_webhook_view,
    pwa_manifest_view,
    pwa_service_worker_view,
    systems_command_center_view,
)

app_name = 'systems'

urlpatterns = [
    path('analytics/', include('apps.systems.analytics.urls')),
    path('audits/', include('apps.systems.audits.urls')),
    path('integrations/', include('apps.systems.integrations.urls')),
    path('portal/', systems_command_center_view, name='command_center'),
    path('portal/external-feed/', external_catalogue_feed_view, name='external_feed'),
    path('portal/external-enquiry/', external_enquiry_webhook_view, name='external_enquiry'),
    path('pwa/manifest.json', pwa_manifest_view, name='pwa_manifest'),
    path('pwa/sw.js', pwa_service_worker_view, name='pwa_sw'),
]
from django.urls import include, path

from apps.logistics.views.logistics_portal_views import (
    logistics_dashboard_view,
    logistics_returns_portal_view,
    warehouse_transfers_portal_view,
)

app_name = 'logistics'

urlpatterns = [
    path('shipments/', include('apps.logistics.shipments.urls')),
    path('warehouse_transfers/', include('apps.logistics.warehouse_transfers.urls')),
    path('portal/', logistics_dashboard_view, name='logistics_dashboard'),
    path('portal/transfers/', warehouse_transfers_portal_view, name='warehouse_transfers_portal'),
    path('portal/returns/', logistics_returns_portal_view, name='logistics_returns_portal'),
]
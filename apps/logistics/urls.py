from django.urls import path, include

app_name = 'logistics'

urlpatterns = [
    path('shipments/', include('apps.logistics.shipments.urls')),
    path('warehouse_transfers/', include('apps.logistics.warehouse_transfers.urls')),
]

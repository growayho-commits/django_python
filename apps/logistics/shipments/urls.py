from django.urls import path
from .views.management_views import create_shipment_view
from .views.shipment_views import LiveShipmentTrackingAPIView
from .views.tracking_views import track_shipment_view

app_name = 'shipments'

urlpatterns = [
    path('create-shipment/', create_shipment_view, name='create_shipment'),
    path('live-shipment-tracking-a-p-i/', LiveShipmentTrackingAPIView.as_view(), name='live_shipment_tracking_a_p_i'),
    path('track-shipment/', track_shipment_view, name='track_shipment'),
]

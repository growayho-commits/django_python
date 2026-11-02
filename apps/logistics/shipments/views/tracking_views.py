# apps/logistics/shipments/views/tracking_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def track_shipment_view(request, shipment_id):
    """
    இயந்திரப் பொருள்கள் மற்றும் உதிரிபாகங்கள் அனுப்புதலைக் (Shipment Tracking) கண்காணிக்கும் வியூ.
    """
    shipment_data = {
        "shipment_id": shipment_id,
        "current_status": "DISPATCHED_FROM_WAREHOUSE",
        "partner": "Logistics Partner",
        "message": "Shipment is in transit to the destination."
    }
    return JsonResponse(shipment_data, status=200)
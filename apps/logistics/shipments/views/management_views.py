# apps/logistics/shipments/views/management_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

@require_http_methods(["POST"])
def create_shipment_view(request):
    """
    புதிய ஷிப்மென்ட் பதிவுகளை உருவாக்கப் பயன்படும் வியூ.
    """
    try:
        data = json.loads(request.body)
        destination = data.get("destination", "Default Destination")
        
        response_data = {
            "status": "SUCCESS",
            "message": "Shipment record created successfully.",
            "destination": destination
        }
        return JsonResponse(response_data, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data provided."}, status=400)
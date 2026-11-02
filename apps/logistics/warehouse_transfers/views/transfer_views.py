# apps/logistics/warehouse_transfers/views/transfer_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def warehouse_transfer_view(request, transfer_id):
    """
    கிடங்குகள் இடையேயான பொருள் மாற்றத்தைக் (Warehouse Transfer Details) காட்டும் வியூ.
    """
    transfer_info = {
        "transfer_id": transfer_id,
        "status": "IN_TRANSIT",
        "source": "Main Godown",
        "destination": "Assembly Plant",
        "item_category": "Industrial Machinery Spares"
    }
    return JsonResponse(transfer_info, status=200)
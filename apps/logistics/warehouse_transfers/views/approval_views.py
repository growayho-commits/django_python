# apps/logistics/warehouse_transfers/views/approval_views.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def approve_transfer_view(request, transfer_id):
    """
    பொருள் மாற்றத்திற்கான அனுமதியை (Transfer Approval) உறுதிப்படுத்தும் வியூ.
    """
    approval_data = {
        "transfer_id": transfer_id,
        "approval_status": "APPROVED",
        "authorized_by": "Superuser / Executive"
    }
    return JsonResponse(approval_data, status=200)
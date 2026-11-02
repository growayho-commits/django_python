import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.logistics.shipments.models import ShipmentProfile[cite: 1]
from apps.logistics.warehouse_transfers.models import WarehouseTransferProfile[cite: 1]

class LiveShipmentTrackingAPIView(APIView):
    def get(self, request, shipment_id):
        try:
            shipment = ShipmentProfile.objects.get(id=shipment_id)
            partner = shipment.partner
            
            # 3rd Party Logistics API Integration
            api_url = f"{partner.api_endpoint}/track?tracking_code={shipment.tracking_code}"
            response = requests.get(api_url, headers={"Authorization": f"Bearer {partner.api_key}"})
            
            if response.status_code == 200:
                tracking_info = response.json()
                shipment.status = tracking_info.get('status', shipment.status)
                shipment.save()
                return Response(tracking_info, status=status.HTTP_200_OK)
            return Response({"error": "டிராக்கிங் தகவலை பெற முடியவில்லை"}, status=response.status_code)
        except ShipmentProfile.DoesNotExist:
            return Response({"error": "ஷிப்மென்ட் விவரம் கிடைக்கவில்லை"}, status=status.HTTP_404_NOT_FOUND)
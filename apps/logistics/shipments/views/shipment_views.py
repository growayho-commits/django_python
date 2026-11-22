from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LiveShipmentTrackingAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({"message": "Live shipment tracking operational"}, status=status.HTTP_200_OK)
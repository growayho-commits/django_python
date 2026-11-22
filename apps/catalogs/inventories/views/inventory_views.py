from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile
from apps.catalogs.inventories.serializers.inventory_serializer import InventorySerializer
from apps.catalogs.inventories.services.inventory_service import InventoryApplicationService

class InventoryListCreateAPIView(APIView):
    def get(self, request):
        inventories = InventoryApplicationService.get_all_inventories()
        serializer = InventorySerializer(inventories, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InventorySerializer(data=request.data)
        if serializer.is_valid():
            inventory = InventoryApplicationService.create_inventory(serializer.validated_data)
            return Response(InventorySerializer(inventory).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
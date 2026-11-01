from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.inventories.serializers.inventory_serializer import InventoryProfileSerializer
from apps.catalogs.inventories.dtos.inventory_dtos import InventoryUpdateDTO
from apps.catalogs.inventories.models.inventory_profile import InventoryProfile
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog

class InventorySyncAPIView(APIView):
    def post(self, request):
        serializer = InventoryProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = InventoryUpdateDTO(**serializer.validated_data)
            try:
                catalog = CoreCatalog.objects.get(id=dto.catalog_id)
                inventory_obj = InventoryProfile.update_stock(
                    catalog_obj=catalog,
                    qty=dto.stock_quantity,
                    threshold=dto.low_stock_threshold,
                    location=dto.warehouse_location
                )
                return Response(InventoryProfileSerializer(inventory_obj).data, status=status.HTTP_200_OK)
            except (CoreCatalog.DoesNotExist, ValueError) as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

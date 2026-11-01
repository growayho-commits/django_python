from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.catalog_statuses.serializers.catalog_status_serializer import CatalogStatusProfileSerializer
from apps.catalogs.catalog_statuses.dtos.catalog_status_dtos import CatalogStatusUpdateDTO
from apps.catalogs.catalog_statuses.services.catalog_status_service import CatalogStatusApplicationService

class CatalogStatusUpdateAPIView(APIView):
    def post(self, request):
        serializer = CatalogStatusProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = CatalogStatusUpdateDTO(**serializer.validated_data)
            try:
                status_obj = CatalogStatusApplicationService.update_catalog_status(dto)
                return Response(CatalogStatusProfileSerializer(status_obj).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

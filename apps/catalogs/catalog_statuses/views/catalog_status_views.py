from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.catalog_statuses.models.catalog_status_profile import CatalogStatusProfile
from apps.catalogs.catalog_statuses.serializers.catalog_status_serializer import CatalogStatusSerializer
from apps.catalogs.catalog_statuses.services.catalog_status_service import CatalogStatusApplicationService

class CatalogStatusListCreateAPIView(APIView):
    def get(self, request):
        statuses = CatalogStatusApplicationService.get_all_statuses()
        serializer = CatalogStatusSerializer(statuses, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogStatusSerializer(data=request.data)
        if serializer.is_valid():
            status_obj = CatalogStatusApplicationService.create_status(serializer.validated_data)
            return Response(CatalogStatusSerializer(status_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
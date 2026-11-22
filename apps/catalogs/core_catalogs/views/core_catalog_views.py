from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.core_catalogs.models.core_catalog_models import CoreCatalogProfile
from apps.catalogs.core_catalogs.serializers.core_catalog_serializer import CoreCatalogSerializer
from apps.catalogs.core_catalogs.services.core_catalog_service import CoreCatalogApplicationService

class CoreCatalogListCreateAPIView(APIView):
    def get(self, request):
        catalogs = CoreCatalogApplicationService.get_all_catalogs()
        serializer = CoreCatalogSerializer(catalogs, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CoreCatalogSerializer(data=request.data)
        if serializer.is_valid():
            catalog = CoreCatalogApplicationService.create_catalog(serializer.validated_data)
            return Response(CoreCatalogSerializer(catalog).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
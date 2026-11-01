from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.catalog_medias.serializers.catalog_media_serializer import CatalogMediaProfileSerializer
from apps.catalogs.catalog_medias.dtos.catalog_media_dtos import CatalogMediaCreateDTO
from apps.catalogs.catalog_medias.services.catalog_media_service import CatalogMediaApplicationService

class CatalogMediaSaveAPIView(APIView):
    def post(self, request):
        serializer = CatalogMediaProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = CatalogMediaCreateDTO(**serializer.validated_data)
            try:
                media_obj = CatalogMediaApplicationService.save_media_suite(dto)
                return Response(CatalogMediaProfileSerializer(media_obj).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

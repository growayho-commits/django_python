from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.catalog_medias.models.catalog_media_profile import CatalogMediaProfile
from apps.catalogs.catalog_medias.serializers.catalog_media_serializer import CatalogMediaSerializer
from apps.catalogs.catalog_medias.services.catalog_media_service import CatalogMediaApplicationService

class CatalogMediaListCreateAPIView(APIView):
    def get(self, request):
        medias = CatalogMediaApplicationService.get_all_medias()
        serializer = CatalogMediaSerializer(medias, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogMediaSerializer(data=request.data)
        if serializer.is_valid():
            media = CatalogMediaApplicationService.create_media(serializer.validated_data)
            return Response(CatalogMediaSerializer(media).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
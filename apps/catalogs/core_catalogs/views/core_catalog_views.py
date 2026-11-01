# apps/catalogs/core_catalogs/views/core_catalog_views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.catalogs.core_catalogs.models.core_catalog_profile import CoreCatalog
from apps.catalogs.core_catalogs.serializers.core_catalog_serializer import CoreCatalogSerializer
from apps.catalogs.core_catalogs.services.core_catalog_service import CoreCatalogService

class CoreCatalogCreateView(APIView):
    def post(request):
        """புதிய கேட்டலாக் பொருளைச் சேர்க்க (Add)"""
        serializer = CoreCatalogSerializer(data=request.data)
        if serializer.is_valid():
            CoreCatalogService.create_catalog_item(serializer.validated_data)
            return Response({"message": "Catalog item created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CoreCatalogUpdateView(APIView):
    def put(self, request, pk):
        """ஏற்கனவே உள்ள கேட்டலாக் பொருளைப் புதுப்பிக்க (Edit / Update)"""
        try:
            serializer = CoreCatalogSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                updated_item = CoreCatalogService.update_catalog_item(pk, serializer.validated_data)
                return Response(CoreCatalogSerializer(updated_item).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
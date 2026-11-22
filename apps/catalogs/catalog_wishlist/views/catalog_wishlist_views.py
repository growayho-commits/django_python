from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.catalog_wishlist.models.catalog_wishlist_profile import CatalogWishlistProfile
from apps.catalogs.catalog_wishlist.serializers.catalog_wishlist_serializer import CatalogWishlistSerializer
from apps.catalogs.catalog_wishlist.services.catalog_wishlist_service import CatalogWishlistApplicationService

class CatalogWishlistListCreateAPIView(APIView):
    def get(self, request):
        wishlists = CatalogWishlistApplicationService.get_all_wishlists()
        serializer = CatalogWishlistSerializer(wishlists, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CatalogWishlistSerializer(data=request.data)
        if serializer.is_valid():
            item = CatalogWishlistApplicationService.create_wishlist_item(serializer.validated_data)
            return Response(CatalogWishlistSerializer(item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.wishlists.serializers.wishlists_serializer import WishlistProfileSerializer
from apps.catalogs.wishlists.dtos.wishlists_dtos import WishlistActionDTO
from apps.catalogs.wishlists.services.wishlists_service import WishlistApplicationService

class WishlistToggleAPIView(APIView):
    def post(self, request):
        serializer = WishlistProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = WishlistActionDTO(**serializer.validated_data)
            wishlist_obj = WishlistApplicationService.add_to_wishlist(dto)
            return Response(WishlistProfileSerializer(wishlist_obj).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

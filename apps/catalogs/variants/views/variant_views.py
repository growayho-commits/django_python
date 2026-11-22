from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.variants.models.variant_profile import *
from apps.catalogs.variants.serializers.variant_serializer import VariantSerializer
from apps.catalogs.variants.services.variant_service import VariantApplicationService

class VariantListCreateAPIView(APIView):
    def get(self, request):
        variants = VariantApplicationService.get_all_variants()
        serializer = VariantSerializer(variants, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = VariantSerializer(data=request.data)
        if serializer.is_valid():
            variant = VariantApplicationService.create_variant(serializer.validated_data)
            return Response(VariantSerializer(variant).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
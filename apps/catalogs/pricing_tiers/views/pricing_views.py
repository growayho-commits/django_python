from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.pricing_tiers.serializers.pricing_serializer import PricingProfileSerializer
from apps.catalogs.pricing_tiers.dtos.pricing_dtos import PricingProfileCreateDTO
from apps.catalogs.pricing_tiers.services.pricing_service import PricingApplicationService

class PricingCreateOrUpdateAPIView(APIView):
    def post(self, request):
        serializer = PricingProfileSerializer(data=request.data)
        if serializer.is_valid():
            dto = PricingProfileCreateDTO(**serializer.validated_data)
            try:
                pricing_obj = PricingApplicationService.create_or_update_pricing(dto)
                return Response(PricingProfileSerializer(pricing_obj).data, status=status.HTTP_200_OK)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from apps.catalogs.pricing_tiers.models.pricing_tier_profile import PricingTierProfile
from apps.catalogs.pricing_tiers.serializers.pricing_tier_serializer import PricingTierSerializer
from apps.catalogs.pricing_tiers.services.pricing_tier_service import PricingTierApplicationService

class PricingTierListCreateAPIView(APIView):
    def get(self, request):
        tiers = PricingTierApplicationService.get_all_tiers()
        serializer = PricingTierSerializer(tiers, many=True)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PricingTierSerializer(data=request.data)
        if serializer.is_valid():
            tier = PricingTierApplicationService.create_tier(serializer.validated_data)
            return Response(PricingTierSerializer(tier).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)